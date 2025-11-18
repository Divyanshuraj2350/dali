#!/usr/bin/env python3
"""
Dali Voice Assistant - Background Service
Listens for wake words and activates the assistant.
"""

import sys
import time
import threading
import speech_recognition as sr
from main import conversation_flow, introduction, read_aloud

class DaliService:
    def __init__(self):
        self.r = sr.Recognizer()
        self.is_active = False
        self.running = True

    def listen_for_wake_word(self):
        """Continuously listen for wake words"""
        print("🎤 Dali is listening in the background...")
        print("💡 Say 'Hey,he,darling,Dali,assistant,okay dali,ok dali,start,computer' to activate")   
        
        wake_words = [
            "computer",
            "okay dali",
            "ok dali",
            "hello dali",
            "hey assistant",
            "assistant",
            "he",
            "hi darling",
            "dali",
            "listen",
        ]

        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
            
            while self.running:
                try:
                    print("\n👂 Listening for wake word...")
                    audio = self.r.listen(source, timeout=3, phrase_time_limit=3)
                    
                    try:
                        text = self.r.recognize_google(audio).lower()
                        print(f"🔊 Heard: {text}")
                        
                        if "hey dali" in text or "listen" in text or "okay dali"in text or "ok dali" in text or "assistant" in text or "okay darling" in text or "hey darling" in text or "he" in text or "computer" in text or "hey dolly" in text or "hi dali" in text:
                            print("✨ Wake word detected! Activating Dali...")
                            self.activate_dali()
                    
                    except sr.UnknownValueError:
                        pass  # Didn't understand, keep listening
                    except sr.RequestError as e:
                        print(f"⚠️  Speech recognition error: {e}")
                        time.sleep(1)
                
                except sr.WaitTimeoutError:
                    pass  # Timeout, keep listening
                except Exception as e:
                    print(f"❌ Error: {e}")
                    time.sleep(1)
    
    def activate_dali(self):
        """Activate Dali and start conversation"""
        if self.is_active:
            return
        
        self.is_active = True
        
        try:
            introduction()
            conversation_flow()
        except KeyboardInterrupt:
            print("\n👋 Dali deactivated")
        except Exception as e:
            print(f"❌ Error in conversation: {e}")
        finally:
            self.is_active = False
            print("\n💤 Dali is back to listening mode...")
    
    def stop(self):
        """Stop the service"""
        self.running = False
        print("\n🛑 Stopping Dali service...")

def main():
    print("="*50)
    print("🤖 DALI VOICE ASSISTANT - Background Service")
    print("="*50)
    
    service = DaliService()
    
    try:
        service.listen_for_wake_word()
    except KeyboardInterrupt:
        service.stop()
        print("\n👋 Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
