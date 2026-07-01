from keywords import keywords

BATCH_SIZE = 20

batches = [
    keywords[i:i+BATCH_SIZE]
    for i in range(0, len(keywords), BATCH_SIZE)
]

print(f"Total Keywords : {len(keywords)}")
print(f"Total Batches  : {len(batches)}")

for i, batch in enumerate(batches, start=1):
    print(f"Batch {i}: {len(batch)} keywords")