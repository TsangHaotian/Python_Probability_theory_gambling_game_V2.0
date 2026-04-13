# Gambling Simulation Warning Program 🎰⚠️

An educational gambling behavior simulator that demonstrates the dangers of gambling through real-time fund curves.

## 🚨 Core Features

### Running Interface

![image](https://github.com/user-attachments/assets/807da92b-15a6-4000-8a16-963f27d487c1)
![image](https://github.com/user-attachments/assets/8f8eb559-5b0b-44b7-957b-5d720407739e)

### Simulation System
- Real-time balance calculation
- Betting history tracking
- Dynamic visualization of fund curves
- Random win/loss probability simulation

### Warning Functions
- Warning messages displayed upon exit
- Visual analysis of fund changes
- Anti-gambling提示信息 (Anti-gambling tips)
- Forced termination when balance reaches zero

## 📊 Fund Curve Analysis

```python
# Fund curve drawing logic
self.chart_ax.plot(self.balance_history, marker='o', color='red')
self.chart_ax.set_title('Fund Change Curve')
self.chart_ax.set_xlabel('Number of Bets')
self.chart_ax.set_ylabel('Balance (Yuan)')
```

**Chart Features**:
- Real-time line chart updates
- Marking each betting point
- Red warning color scheme
- Grid auxiliary lines

## ⚠️ Exit Warning

```python
# Exit prompt logic
messagebox.showinfo('Game Over', 
    'The boss beat you up and took all your remaining time!\n\n'
    'Important Reminder: Nine out of ten gamblers lose; long-term gambling guarantees loss. Stay away from gambling!')
```

## 🛠️ Technical Implementation

### Main Components
- **GUI Framework**: Tkinter
- **Data Visualization**: Matplotlib
- **Interaction Prompts**: Messagebox
- **Random Algorithm**: Python random

### Core Class Methods
- `quit_game()` - Handles exit logic
- `show_balance_chart()` - Initializes fund curve
- `update_balance_chart()` - Refreshes chart data

## 🚀 Quick Start

```bash
pip install matplotlib numpy
python main.py
```

## 📌 Usage Instructions

1. Launch to display the gambling simulation interface
2. Update fund balance with each bet
3. View real-time fund change curve
4. Display warning information upon exit

## 💡 Design Purpose

By simulating the fund change process of gambling:
- Intuitively demonstrate the mathematical law of "long-term gambling leads to inevitable losses"
- Reveal gambling risks using data visualization
- Reinforce the warning effect of "stay away from gambling"
---

⭐ **Do not use for real gambling**  
⚠️ This program is for educational warning purposes only
