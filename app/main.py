#!/usr/bin/env python3
import os
from nicegui import ui, html, app
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
                ui.label(character.error).bind_visibility_from(character, 'error')
                ui.label(cuisine.error).bind_visibility_from(cuisine, 'error')
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
                            with ui.row().classes('flex items-center flex-nowrap'):
                                ui.icon('favorite')
                                ui.label(item).classes('text-sm')

            ui.label(tour_data.conclusion).classes('text-lg mt-4')

    cuisine_options = ['Italian', 'Mexican', 'Chinese', 'Japanese', 'Indian', 'Thai', 'French', 'Greek', 'Mediterranean', 'American', 'Korean', 'Southern', 'BBQ']

    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')
    ui.dark_mode().bind_value(app.storage.user, 'dark_mode')

    with html.header().classes('w-full flex justify-between'):
        lft_logo(app.storage.user['dark_mode'])
        ui.checkbox('Dark Mode', on_change=lambda e: lft_logo.refresh(e.value)).bind_value(app.storage.user, 'dark_mode')

    with html.section().classes('w-full max-w-4xl mx-auto text-center p-10 border rounded-2xl'):
        ui.label('Lit Food Tours').classes('w-full text-2xl font-bold mt-4')
        ui.label('Let AI plan a food tour for you and one of your favorite characters and go on an imaginative culinary adventure!').classes('w-full text-lg mt-2')
        ui.label('What Southern favorites would Sherlock Holmes enjoy? What about Hello Kitty on a Mexican vacation? Imagine Thor eating Thai?').classes('w-full text-lg mt-2')

        with ui.row().classes('flex pt-10'):
            character = ui.input(
                placeholder='Enter a character name',
                validation=lambda value: 'Character name too short' if len(value) < 3 else None,
            ).props('rounded outlined dense').classes('grow')
            cuisine = ui.select(
                options=cuisine_options,
                value=cuisine_options[0],
                with_input=True, 
                new_value_mode='add-unique',
                validation=lambda value: 'Cuisine should not be empty' if value is None else None,
            ).props('rounded outlined dense').classes('grow')
            ui.button(
                'Let\'s Eat!', on_click=lambda: submit_form(character, cuisine)
            ).props('rounded outline').classes('self-start grow md:grow-0').bind_enabled_from(character, 'value')

    tour_container = ui.column().classes('w-full mt-4 max-w-4xl mx-auto p-10 border rounded-2xl')
    tour_container.set_visibility(False)

    with html.footer().classes('mt-auto'):
        ui.label('Made with AI - An Experiment by Andrew').classes('text-xs text-stone-400')

ui.add_head_html('''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XJC1W1JEGJ"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-XJC1W1JEGJ');
    </script>
''')

ui.add_head_html('<meta name="description" content="Fun AI experiment where you create imaginary food tours with your favorite characters!" />')

ui.run(
    port=8080,
    title='Literary Food Tour',
    storage_secret=os.environ['STORAGE_SECRET'],
)
