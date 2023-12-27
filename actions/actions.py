from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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
        else:
            dispatcher.utter_message(text="I'm sorry, I'd not detect your choice.")
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
        else:
            dispatcher.utter_message(text="I'm sorry, I'd not detect your choice.")
        return []
