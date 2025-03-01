"""
This script has been generated by modeci_mdf v0.4.9.
It is an export of a MDF model (mdf.s - MDF stateful, i.e. full MDF allowing stateful parameters) to PyTorch

"""

import torch
import torch.nn as nn
import onnx
import onnxruntime as rt
from math import *


class input0(nn.Module):
    def __init__(
        self,
        input_level=torch.tensor(0.0),  # orig type: <class 'float'>
    ):
        super().__init__()
        self.input_level = input_level
        self.execution_count = torch.tensor(0)

    def forward(
        self,
    ):
        self.execution_count = self.execution_count + torch.tensor(1)
        return self.input_level


class A(nn.Module):
    def __init__(
        self,
        slope=torch.tensor(1.1),  # orig type: <class 'float'>
        intercept=torch.tensor(1.2),  # orig type: <class 'float'>
    ):
        super().__init__()
        self.slope = slope
        self.intercept = intercept
        self.execution_count = torch.tensor(0)

    def forward(
        self,
        input_port1,
    ):
        self.execution_count = self.execution_count + torch.tensor(1)
        linear_func = input_port1 * self.slope + self.intercept
        return linear_func


class B(nn.Module):
    def __init__(
        self,
        gain=torch.tensor(2.1),  # orig type: <class 'float'>
        bias=torch.tensor(2.2),  # orig type: <class 'float'>
        offset=torch.tensor(2.3),  # orig type: <class 'float'>
    ):
        super().__init__()
        self.gain = gain
        self.bias = bias
        self.offset = offset
        self.execution_count = torch.tensor(0)

    def forward(
        self,
        input_port1,
    ):
        self.execution_count = self.execution_count + torch.tensor(1)
        logistic_func = 1 / (
            1 + exp(-1 * self.gain * (input_port1 + self.bias) + self.offset)
        )
        return logistic_func


class C(nn.Module):
    def __init__(
        self,
        scale=torch.tensor(3.1),  # orig type: <class 'float'>
        rate=torch.tensor(3.2),  # orig type: <class 'float'>
        bias=torch.tensor(3.3),  # orig type: <class 'float'>
        offset=torch.tensor(3.4),  # orig type: <class 'float'>
    ):
        super().__init__()
        self.scale = scale
        self.rate = rate
        self.bias = bias
        self.offset = offset
        self.execution_count = torch.tensor(0)

    def forward(
        self,
        input_port1,
    ):
        self.execution_count = self.execution_count + torch.tensor(1)
        exponential_func = (
            self.scale * exp((self.rate * input_port1) + self.bias) + self.offset
        )
        return exponential_func


class D(nn.Module):
    def __init__(
        self,
        scale=torch.tensor(4.0),  # orig type: <class 'float'>
    ):
        super().__init__()
        self.scale = scale
        self.execution_count = torch.tensor(0)

    def forward(
        self,
        input_port1,
    ):
        self.execution_count = self.execution_count + torch.tensor(1)
        sin_func = self.scale * sin(input_port1)
        return sin_func


class Model(nn.Module):
    def __init__(
        self,
        input0,
        A,
        B,
        C,
        D,
    ):
        super().__init__()
        self.input0 = input0
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def forward(self, input):
        val_input0 = torch.zeros_like(input)
        val_A = torch.zeros_like(input)
        val_B = torch.zeros_like(input)
        val_C = torch.zeros_like(input)
        val_D = torch.zeros_like(input)

        val_input0 = val_input0 + self.input0()
        val_A = val_A + self.A(val_input0)
        val_B = val_B + self.B(val_A)
        val_C = val_C + self.C(val_B)
        val_D = val_D + self.D(val_C)

        return (
            val_input0,
            val_A,
            val_B,
            val_C,
            val_D,
        )


model = Model(
    input0=input0(),
    A=A(),
    B=B(),
    C=C(),
    D=D(),
)
model = torch.jit.script(model)
dummy_input = torch.tensor(
    0.0,
)
output = model(dummy_input)
torch.onnx.export(
    model, dummy_input, "ABCD.onnx", verbose=True, input_names=[], opset_version=9
)
onnx_model = onnx.load("ABCD.onnx")
onnx.checker.check_model(onnx_model)
sess = rt.InferenceSession("ABCD.onnx")
res = sess.run(
    None,
    {sess.get_inputs()[0].name: dummy_input.numpy()}
    if len(sess.get_inputs()) > 0
    else {},
)

if __name__ == "__main__":
    print("Exported to PyTorch and ONNX")
