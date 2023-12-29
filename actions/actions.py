import arrow
import dateparser

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


city_db = {
    "brussels": "Europe/Brussels",
    "zagreb": "Europe/Zagreb",
    "london": "Europe/London",
    "lisbon": "Europe/Lisbon",
    "amsterdam": "Europe/Amsterdam",
    "seattle": "US/Pacific",
}


class ActionTellTime(Action):
    def name(self) -> Text:
        return "action_tell_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place."
            dispatcher.utter_message(text=msg)
            return []

        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"I don't recognize {current_place}, is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)
        return []


class extractFoodEntity(Action):
    def name(self) -> Text:
        return "action_extract_food_entity"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        food_entity = next(tracker.get_latest_entity_values("food"), None)

        if food_entity:
            dispatcher.utter_message(
                text=f"You have selected {food_entity} as your choice."
            )
            return []
        else:
            dispatcher.utter_message(text=f"I'm sorry, I'd not detect your choice.")
            return []


class orderFoodAction(Action):
    def name(self) -> Text:
        return "action_order_food"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Sure, which kinda food would you like to order?")
        return []


class confirmOrderAction(Action):
    def name(self) -> Text:
        return "action_confirm_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        food_entity = next(tracker.get_latest_entity_values("food"), None)

        if food_entity:
            dispatcher.utter_message(text=f"I've ordered {food_entity} for you.")
            return []
        else:
            dispatcher.utter_message(text=f"I'm sorry, I'd not detect your choice.")
            return []
