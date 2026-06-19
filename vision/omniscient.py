import cv2
import numpy as np
import asyncio
import time
from vision.screen_reader import ScreenReader

class OmniscientVision:
    def __init__(self):
        self.screen_reader = ScreenReader()
        self.active = False
        self.frame_buffer = []
        self.max_buffer = 30

    async def start_stream(self):
        self.active = True
        print("Friday: Omniscient Vision stream initialized. Processing real-time world-state...")
        while self.active:
            # get_screen_data is sync but lightweight, if it becomes slow it should be run in a thread
            frame = self.screen_reader.get_screen_data()
            self.frame_buffer.append(np.array(frame))
            if len(self.frame_buffer) > self.max_buffer:
                self.frame_buffer.pop(0)

            self.analyze_environment()
            await asyncio.sleep(0.1) # FIXED: Use asyncio.sleep instead of time.sleep

    def analyze_environment(self):
        pass

    def get_world_state(self):
        return {
            "active": self.active,
            "buffer_size": len(self.frame_buffer),
            "last_analysis": time.time()
        }

    def stop_stream(self):
        self.active = False
        print("Friday: Omniscient Vision stream terminated.")
