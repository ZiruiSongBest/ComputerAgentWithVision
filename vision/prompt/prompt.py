prompt = {
        "default": "What's in the image? Please provide a description of the image and any relevant details.",
        "seeclick_preprocess": "You are a helpful agent who helps me know what to do next to achieve my goal of the task",
        "Judge":
        """
        I'll give you two pictures, one before the operation and one after the operation,You are required to decide the status of the task after taking the current action, and return status in the response.
        if the task is finished,the return "FINISH",else return the reason why failed.
        The task is     
        """,
}