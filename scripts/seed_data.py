import asyncio
import json
import os
from datetime import datetime

from src.api.dependencies import get_emb_service
from src.db.database import async_session_maker
from src.db.models.content import Category, Content, ContentCreate


async def seed_data():
    async with async_session_maker() as session:
        emb_service = await get_emb_service()
        # We need to manually handle the session for ContentService if we want to use it
        # ContentService expects an AsyncSession.

        data_dir = "data"
        if not os.path.exists(data_dir):
            print(f"Directory {data_dir} not found.")
            return

        category_map = {
            "scholarship.json": Category.SCHOLARSH,
            "news.json": Category.NEW,
            "announcements.json": Category.ANN,
        }

        for filename in os.listdir(data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(data_dir, filename)
                category = category_map.get(filename, Category.INFO)

                print(f"Processing {file_path} as {category}...")

                with open(file_path, "r", encoding="utf-8") as f:
                    items = json.load(f)

                if not items:
                    continue

                # Prepare texts for batch embedding
                texts_to_embed = []
                content_payloads = []

                for item in items:
                    # Replicate the text construction from ContentService.create_content
                    # We use the emb_service to pre-process the text
                    processed_title = emb_service.pre_process_text(item["title"])
                    processed_summary = emb_service.pre_process_text(item["summary"])
                    processed_content = emb_service.pre_process_text(item["content"])

                    text_content = (
                        f"#{processed_title}\n\n"
                        f"## Summary\n{processed_summary}\n\n"
                        f"## Content\n{processed_content}"
                    )

                    texts_to_embed.append(text_content)

                    # Prepare the content creation payload
                    # Note: we need to parse the date string to datetime
                    post_date = datetime.fromisoformat(item["post_date"])

                    content_payloads.append(
                        {
                            "title": item["title"],
                            "summary": item["summary"],
                            "category": category,
                            "content": item["content"],
                            "post_date": post_date,
                        }
                    )

                # Batch embed all texts in this file
                print(f"Generating embeddings for {len(texts_to_embed)} items...")
                embeddings = emb_service.embed_many_texts(texts_to_embed)

                # Insert into database
                for i, payload in enumerate(content_payloads):
                    content_in = ContentCreate(**payload)

                    # Create the Content object
                    new_content = Content(**content_in.model_dump())
                    new_content.embedding = embeddings[i]

                    session.add(new_content)

                await session.commit()
                print(f"Successfully seeded {len(content_payloads)} items from {filename}.")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_data())
