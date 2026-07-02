from db_helpers import get_collection_progress

progress = get_collection_progress(1)

print("Total stickers:", progress[0])
print("Collected stickers:", progress[1])
print("Missing stickers:", progress[2])
print("Completion percentage:", progress[3], "%")