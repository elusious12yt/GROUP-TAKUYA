import tkinter as tk
import csv
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        self.root.geometry("400x300")
        
        self.flashcards = []
        self.load_flashcards('flashcards.csv')
        
        self.main_menu()
    
    def load_flashcards(self, filename):
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.flashcards = [{'question': row['question'], 'answer': row['answer']} for row in reader if 'question' in row and 'answer' in row]
        except FileNotFoundError:
            print(f"File {filename} not found. Please ensure the file exists.")
    
    def main_menu(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Flashcard Quiz App", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Add a Flashcard", font=("Arial", 14), command=self.add_flashcard).pack(pady=5)
        tk.Button(self.root, text="Take the Quiz", font=("Arial", 14), command=self.start_quiz).pack(pady=5)
        tk.Button(self.root, text="Create or Reset Flashcards File", font=("Arial", 14), command=self.create_reset_file).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.exit_app).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def add_flashcard(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Add a Flashcard", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Question:", font=("Arial", 12)).pack(pady=5)
        question_entry = tk.Entry(self.root, width=40)
        question_entry.pack(pady=5)
        
        tk.Label(self.root, text="Answer:", font=("Arial", 12)).pack(pady=5)
        answer_entry = tk.Entry(self.root, width=40)
        answer_entry.pack(pady=5)
        
        def save_flashcard():
            question = question_entry.get().strip()
            answer = answer_entry.get().strip()
            with open('flashcards.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['question', 'answer'])
                writer.writerow({'question': question, 'answer': answer})
            # Automatically return to main menu after adding a flashcard
            self.main_menu()
        
        tk.Button(self.root, text="Save", font=("Arial", 12), command=save_flashcard).pack(pady=5)
    
    def create_reset_file(self):
        with open('flashcards.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['question', 'answer'])
            writer.writeheader()
        tk.Label(self.root, text="Flashcards file created/reset successfully!", font=("Arial", 12)).pack(pady=5)
        self.flashcards.clear()  # Clear in-memory list as well
    
    def start_quiz(self):
        if not self.flashcards:
            tk.Label(self.root, text="No flashcards available. Add some first.", font=("Arial", 12)).pack(pady=5)
        else:
            self.current_index = 0
            self.score = 0
            random.shuffle(self.flashcards)
            self.show_question()
    
    def show_question(self):
        self.clear_screen()
        
        if self.current_index < len(self.flashcards):
            card = self.flashcards[self.current_index]
            question = card['question']
            self.time_remaining = 15  # 15 seconds per question
            
            tk.Label(self.root, text=f"Question: {question}", font=("Arial", 14), wraplength=350).pack(pady=10)
            self.answer_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
            self.answer_entry.pack(pady=10)
            
            self.timer_label = tk.Label(self.root, font=("Arial", 12))
            self.timer_label.pack(pady=10)
            
            # Define a function to check the answer and move to the next question
            def check_answer():
                answer = self.answer_entry.get().strip().lower()
                correct_answer = card['answer'].strip().lower()
                if answer == correct_answer:
                    self.score += 1
                    self.show_feedback("Correct!")
                else:
                    self.show_feedback(f"Incorrect! The correct answer was: {card['answer']}")
            
            tk.Button(self.root, text="Submit", font=("Arial", 12), command=check_answer).pack(pady=5)
            
            # Exit Quiz button to go back to the main menu
            tk.Button(self.root, text="Exit Quiz", font=("Arial", 12), command=self.main_menu).pack(pady=5)
            
            # Start the countdown timer
            self.update_timer()
        else:
            self.show_score()

    def update_timer(self):
        if self.time_remaining > 0:
            self.timer_label.config(text=f"Time remaining: {self.time_remaining}")
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            # Display the correct answer and proceed
            card = self.flashcards[self.current_index]
            self.show_feedback(f"Time's up! The correct answer was: {card['answer']}")
    
    def show_feedback(self, message):
        self.clear_screen()
        tk.Label(self.root, text=message, font=("Arial", 14)).pack(pady=10)
        self.current_index += 1
        # Wait 2 seconds before showing the next question
        self.root.after(2000, self.show_question)
    
    def show_score(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Quiz finished! Your score is {self.score}/{len(self.flashcards)}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 12), command=self.main_menu).pack(pady=5)

    def exit_app(self):
        self.root.destroy()  # Ensure proper exit from the application

root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()
