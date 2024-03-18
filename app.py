import matplotlib.pyplot as plt
import numpy as np


# Inputs
coin_name = 'TEST'
total_supply = 1000000
unlock_schedule = [
    {
        'name': 'team',
        'percent': 10,
        'cliff': 0,
        'duration': 12
    },
    {
        'name': 'investors',
        'percent': 30,
        'cliff': 6,
        'duration': 12        
    },
    {
        'name': 'community',
        'percent': 60,
        'cliff': 0,
        'duration': 24        
    }
]


# Calculate total vesting period based on max vesting period in tokenomics
total_vesting_period = max([(schedule['duration'] + schedule['cliff']) for schedule in unlock_schedule])
months_list = [i for i in range(1, total_vesting_period + 1)]


# Create unlocked schedule
for category in unlock_schedule:
    category['category_supply'] = total_supply * category['percent'] / 100
    category['unlocked_supply'] = []
    
    # Add 0 coins while cliff
    for month in range(1, category['cliff'] + category['duration'] + 1):
        if month <= category['cliff']:
            category['unlocked_supply'].append(0)  # No tokens unlocked during the cliff period
        else:
            category['unlocked_supply'].append(category['category_supply'] / category['duration'])
    
    # Add 0 coins if the unlock schedule ended earlier than the total unlock schedule
    while len(category['unlocked_supply']) < len(months_list):
        category['unlocked_supply'].append(0)


# Create new dict for plot
plot_schedule = {}
for category in unlock_schedule:
    new_key = category['name']
    new_value = category['unlocked_supply']
    plot_schedule[new_key] = [sum(new_value[:i+1]) for i in range(len(new_value))]


# Chart
# Create plot
fig, ax = plt.subplots()
ax.stackplot(months_list, plot_schedule.values(), labels=plot_schedule.keys(), alpha=0.8)

# Plot text
ax.legend(loc='upper left', reverse=True)
ax.set_title(f'Token unlocks for {coin_name}')
ax.set_xlabel('Month')
ax.set_ylabel('Number of coins')

# Plot formats
plt.ticklabel_format(style='plain', axis='y') # Format the number from 1e6 to 1000000
plt.grid(True, which='both', linestyle='-', linewidth=0.5, color='gray') # Show grid
# plt.xticks(np.arange(1, months_list, step=6)) # Change the number of ticks on x axis


# Print chart
plt.show()         