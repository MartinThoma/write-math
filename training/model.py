"""CNN used for symbol recognition. export.py relies on the exact module
layout (Conv-BN-ReLU blocks, MaxPool, Linear) to fold BatchNorm and emit the
layer list understood by docs/js/nn.js."""

import torch
from torch import nn

from raster import SIZE


def block(cin, cout):
    return [nn.Conv2d(cin, cout, 3, padding=1, bias=False), nn.BatchNorm2d(cout), nn.ReLU(inplace=True)]


class SymbolNet(nn.Module):
    def __init__(self, n_classes, widths=(32, 64, 128), hidden=256, dropout=0.4):
        super().__init__()
        layers, cin = [], 1
        for w in widths:
            layers += block(cin, w) + block(w, w) + [nn.MaxPool2d(2)]
            cin = w
        self.features = nn.Sequential(*layers)
        side = SIZE // 2 ** len(widths)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(cin * side * side, hidden),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden, n_classes),
        )
        self.config = {"n_classes": n_classes, "widths": list(widths), "hidden": hidden, "dropout": dropout}

    def forward(self, x):
        return self.classifier(self.features(x))
