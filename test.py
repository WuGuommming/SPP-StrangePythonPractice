import torch
import torch.nn.functional as F

x = torch.tensor([[0.1, 0.3],
                  [0.4, 0.2],
                  [0.3, 0.1]])

q = torch.tensor([[1., 0.],
                  [0., 1.]])
k = torch.tensor([[1., 0.],
                  [0., 1.]])
v = torch.tensor([[0.535, 0.065],
                  [0.025, 0.545]])
q.requires_grad = True
k.requires_grad = True
v.requires_grad = True

Q = torch.matmul(x, q)
K = torch.matmul(x, k)
V = torch.matmul(x, v)
print(Q)
print(K)
print(V)
tt = torch.matmul(Q, torch.transpose(K, 0, 1))
tt = tt / pow(x.size()[1], 1/2)
print(tt)
A = torch.softmax(tt, dim=1)
print(A)
A = torch.matmul(A, V)
print(A)

T = torch.tensor([[0.5, 0.8],
                  [0.1, 0.3],
                  [0.6, 0.6]])

loss = F.mse_loss(A, T)
print(loss)
loss.backward()

print(q.grad)
print(k.grad)
print(v.grad)

q = q - q.grad * 0.5
k = k - k.grad * 0.5
v = v - v.grad * 0.5


Q = torch.matmul(x, q)
K = torch.matmul(x, k)
V = torch.matmul(x, v)

tt = torch.matmul(Q, torch.transpose(K, 0, 1))
tt = tt / pow(x.size()[1], 1/2)
A = torch.softmax(tt, dim=1)
A = torch.matmul(A, V)

T = torch.tensor([[0.5, 0.8],
                  [0.1, 0.3],
                  [0.6, 0.6]])

loss = F.mse_loss(A, T)
print(loss)
