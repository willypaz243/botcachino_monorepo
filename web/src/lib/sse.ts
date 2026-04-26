export interface SSEEvent {
  content: string;
  type: "text" | "error" | "info";
  done: boolean;
}

export function streamSSE(
  url: string,
  options: globalThis.RequestInit,
  onEvent: (event: SSEEvent) => void,
  onDone?: () => void,
  onError?: (error: Error) => void,
): () => void {
  const cancelledRef = { value: false };

  (async () => {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          Accept: "text/event-stream",
          "Content-Type": "application/json",
          "X-API-Key": import.meta.env.VITE_API_KEY || "",
          ...options.headers,
        },
      });

      if (!response.body) {
        throw new Error("ReadableStream not supported in this browser");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = "";

      while (!cancelledRef.value) {
        const { done, value } = await reader.read();

        if (done || cancelledRef.value) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();

          if (!trimmed.startsWith("data:")) {
            continue;
          }

          const payload = trimmed.slice(5).trimStart();

          if (payload.length === 0) {
            continue;
          }

          try {
            const event: SSEEvent = JSON.parse(payload);
            onEvent(event);

            if (event.done) {
              onDone?.();
              break;
            }
          } catch {
            console.error("Failed to parse SSE JSON:", payload);
          }
        }
      }
    } catch (error) {
      const err = error instanceof Error ? error : new Error(String(error));
      onError?.(err);
    }
  })();

  const cancel = () => {
    cancelledRef.value = true;
  };

  return cancel;
}
