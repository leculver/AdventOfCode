import torch

with open("04_input.txt") as f:
    wordsearch = [x.strip() for x in f.readlines()]


H = len(wordsearch)
W = len(wordsearch[0])
grid = torch.empty(H, W, dtype=torch.int8)
for i in range(H):
    for j in range(W):
        grid[i, j] = ord(wordsearch[i][j])

device = "cuda" if torch.cuda.is_available() else "cpu"
grid = grid.to(device)

print(f"device: {device}")

# Create a 3x3 sliding window view of the grid.  This is of shape H-2, W-2, 3, 3
windows = grid.unfold(0, size=3, step=1).unfold(1, size=3, step=1)

pos_a = windows[..., 1, 1] == ord('A')
print(pos_a.T)

pos_diag = ((windows[..., 0, 0] == ord('M')) & (windows[..., 2, 2] == ord('S'))) | \
           ((windows[..., 0, 0] == ord('S')) & (windows[..., 2, 2] == ord('M')))


pos_anti = ((windows[..., 2, 0] == ord('M')) & (windows[..., 0, 2] == ord('S'))) | \
           ((windows[..., 2, 0] == ord('S')) & (windows[..., 0, 2] == ord('M')))


print(pos_diag.T)
print(pos_anti.T)

result = pos_a & pos_diag & pos_anti
print(result.T)
total = result.sum()
print(f"total: {total} device={device}")
