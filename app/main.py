#!/usr/bin/env python3
from nicegui import ui

@ui.page('/')
def main():
    return ui.label('Hello World')

ui.run(title='Hello World')
