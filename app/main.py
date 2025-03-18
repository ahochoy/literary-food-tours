#!/usr/bin/env python3
from nicegui import ui, html
from ai_foodie_planner import get_food_tour
from assets.logo import lft_logo

@ui.page('/')
def main():
    async def submit_form(character, cuisine):

        tour_container.clear()
        tour_container.set_visibility(True)

        with tour_container:
            ui.spinner('dots')

        if (character.error or cuisine.error):
            with tour_container:
                ui.label('Please enter a valid character and cuisine.')
            return

        tour_data = get_food_tour(character=character.value, cuisine=cuisine.value)

        tour_container.clear()
        with tour_container:
            ui.label(tour_data.title).classes('text-xl font-bold mt-4')
            ui.label(tour_data.introduction).classes('text-lg mt-2 mb-4')

            for restaurant in tour_data.restaurants:
                with ui.card().classes('w-full no-shadow border'):
                    ui.label(restaurant.name).classes('text-md font-bold')
                    ui.label(restaurant.description)
                    with ui.row().classes('flex'):
                        for item in restaurant.menu_items:
                            with ui.row().classes('flex items-center'):
                                ui.icon('favorite')
                                ui.label(item)

            ui.label(tour_data.conclusion).classes('text-lg mt-4')

    cuisine_options = ['Italian', 'Mexican', 'Chinese', 'Japanese', 'Indian', 'Thai', 'French', 'Greek', 'Mediterranean', 'American', 'Korean', 'Southern', 'BBQ']

    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')


    with html.header():
        lft_logo().classes('max-w-xs')

    with html.section().classes('w-full max-w-4xl mx-auto text-center p-10 border border-stone-400 bg-stone-50 rounded-2xl'):
        ui.label('Literary Food Tour').classes('w-full text-2xl font-bold mt-4')
        ui.label('Plan a food tour for a literary character and decide what type of food you will eat.').classes('w-full text-lg mt-2')

        with ui.row().classes('flex pt-10'):
            character = ui.input(
                placeholder='Enter a character name',
                validation=lambda value: 'Character name too short' if len(value) < 3 else None,
            ).props('rounded outlined dense bg-color="white"').classes('grow')
            cuisine = ui.select(
                options=cuisine_options,
                value=cuisine_options[0],
                with_input=True, 
                new_value_mode='add-unique',
                validation=lambda value: 'Cuisine should not be empty' if value is None else None,
            ).props('rounded outlined dense bg-color="white"').classes('grow')
            ui.button(
                'Let\'s Eat!', on_click=lambda: submit_form(character, cuisine)
            ).props('rounded outline').classes('self-start').bind_enabled_from(character, 'value')

    tour_container = ui.column().classes('w-full mt-4 max-w-4xl mx-auto p-10 border border-stone-400 bg-stone-50 rounded-2xl')
    tour_container.set_visibility(False)

    with html.footer().classes('mt-auto'):
        ui.label('Made with Love - An Experiment by Andrew').classes('text-xs text-stone-400')

ui.run(port=80, title='Literary Food Tour')
