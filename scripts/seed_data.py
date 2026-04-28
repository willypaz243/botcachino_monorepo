import asyncio
import json
import os
from datetime import datetime

from sqlmodel import select

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
            "informations.json": Category.INFO,
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

                existing_titles_query = await session.execute(
                    select(Content.title).where(Content.category == category)
                )
                existing_titles = set(existing_titles_query.scalars().all())

                # Prepare texts for batch embedding
                texts_to_embed = []
                content_payloads = []

                for item in items:
                    title = item.get("title", "").strip() if item.get("title") else ""
                    summary = item.get("summary", "").strip() if item.get("summary") else ""
                    content = item.get("content", "").strip() if item.get("content") else ""
                    post_date_str = (
                        item.get("post_date", "").strip() if item.get("post_date") else ""
                    )

                    if not title or not summary or not content or not post_date_str:
                        print(f"Ignoring item with missing fields: {title[:30]}")
                        continue

                    if len(title) < 2 or len(title) > 200 or len(summary) < 2 or len(summary) > 500:
                        print(f"Ignoring item with out of bounds length: {title[:30]}")
                        continue

                    if title in existing_titles:
                        print(f"Ignoring duplicated item: {title[:30]}")
                        continue

                    try:
                        post_date = datetime.fromisoformat(post_date_str)
                    except ValueError:
                        print(f"Ignoring item with invalid date: {title[:30]}")
                        continue

                    existing_titles.add(title)

                    # Replicate the text construction from ContentService.create_content
                    # We use the emb_service to pre-process the text
                    processed_title = emb_service.pre_process_text(title)
                    processed_summary = emb_service.pre_process_text(summary)

                    text_content = f"#{processed_title}\n## Summary\n{processed_summary}\n"

                    texts_to_embed.append(text_content)

                    # Prepare the content creation payload
                    # Note: we need to parse the date string to datetime
                    content_payloads.append(
                        {
                            "title": title,
                            "summary": summary,
                            "category": category,
                            "content": content,
                            "post_date": post_date,
                        }
                    )

                if not texts_to_embed:
                    print(f"Skipping {filename}, no items to insert.")
                    continue

                # Batch embed all texts in this file
                print(f"Generating embeddings for {len(texts_to_embed)} items...")
                embeddings = await emb_service.embed_many_texts(texts_to_embed)

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
