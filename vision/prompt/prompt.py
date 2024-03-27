prompt = {
        "default": "What's in the image? Please provide a description of the image and any relevant details.",
        "seeclick_preprocess": "You are a helpful agent who helps me know what to do next to achieve my goal of the task",
        "Judge":
        """
        I'll give you two pictures, one before the operation and one after the operation,You are required to decide the status of the task after taking the current action, and return status in the response.
        if the task is finished,the return "FINISH",else return the reason why failed.
        The task is     
        """,
        
        "decompose_system": 
'''
You are a helpful assistant, who read the previous executed task information, current screenshot, and the task you would like to decompose into more executable tasks. Please help me to decompose the task, the decomposed task should be one of following types: Click, Enter, Scroll, Observe. Return in a json formatted string. Here's are some examples:

"use google to search 'Friends series', and return the rating of IMDb"

{
    "click_the_search_box": {
        "name": "click_the_search_box",
        "description": "Click the search box and prepare to enter",
        "dependencies": [
        ],
        "type": "Click",
        "content": "Search Google or type a URL"
    },
    "enter_weather": {
        "name": "enter_weather",
        "description": "enter weather into the search box",
        "dependencies": [
            "click_the_search_box"
        ],
        "type": "Enter",
        "content": "weather for today"
    },
    "press_enter_to_navigate": {
        "name": "press_enter_to_navigate",
        "description": "press Enter to navigate to the weather",
        "dependencies": [
            "enter_weather"
        ],
        "type": "Enter",
        "content": "<Enter>"
    },
    "observe_current_screen": {
        "name": "observe_current_screen",
        "description": "get the weather for today",
        "dependencies": [
            "press_enter_to_navigate"
        ],
        "type": "Observe",
        "content": "What's the weather today?"
    }
}

A null dictionary should be returned if the task is finished already.
```json
{
    
}
```

remember, each step should be clear, and do what the task requires you to do.
'''
}