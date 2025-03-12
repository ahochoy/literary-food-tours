#!/usr/bin/env python3
from nicegui import ui

@ui.page('/')
def main():

    cuisine_options = ['Italian', 'Mexican', 'Chinese', 'Japanese', 'Indian', 'Thai', 'French', 'Greek', 'Mediterranean', 'American', 'Korean', 'Southern', 'BBQ']

    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full max-w-5xl mx-auto p-4')

    ui.label('Literary Food Tour').classes('w-full text-2xl font-bold mt-4')

    with ui.grid(columns='1fr 1fr fit-content(10%)').classes('w-full'):
        character = ui.input(placeholder='start typing').props('rounded outlined dense')
        cuisine = ui.select(options=cuisine_options, with_input=True).props('rounded outlined dense')
        ui.button('Let\'s Eat!', on_click=lambda: result.set_text(f'Planning: {cuisine.value} food tour for {character.value}')).props('rounded outline')   

    result = ui.label().classes('w-full text-center mt-4') 

ui.run(title='Literary Food Tour')
