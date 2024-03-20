import matplotlib.pyplot as plt
import numpy as np

# Inputs
coin_name = 'TEST'
total_supply = 1000000
unlock_schedule = [
    {
        'name': 'team',
        'percent': 10,
        'tge_percent': 40, # tge percentage is percentage of category percentage
        'cliff': 0,
        'duration': 6
    },
    {
        'name': 'investors',
        'percent': 30,
        'tge_percent': 0,
        'cliff': 6,
        'duration': 12        
    },
    {
        'name': 'community',
        'percent': 60,
        'tge_percent': 0,
        'cliff': 0,
        'duration': 12        
    }
]

# Calculate total vesting period based on max vesting period in tokenomics
total_vesting_period = max([(schedule['duration'] + schedule['cliff']) for schedule in unlock_schedule])
months_list = [i for i in range(total_vesting_period + 1)]

# Create unlocked schedule
for category in unlock_schedule:

    # Create categories for calculating supply for different stages
    category['category_supply'] = total_supply * category['percent'] / 100 # to be used in 'tge_supply' and 'remaining_supply'
    category['tge_supply'] = category['category_supply'] * category['tge_percent'] / 100
    category['vesting_supply'] = category['category_supply'] - category['tge_supply']
    category['unlocked_supply'] = []
    
    # Create unlocks list with tge, cliff, vesting
    for month in range(0, category['cliff'] + category['duration'] + 1):
        
        # TGE amount at month 0
        if month == 0 and category['tge_percent'] > 0:
            category['unlocked_supply'].append(category['tge_supply'])
        
        # Amount s0 while cliff
        elif month <= category['cliff'] + 1 :
            category['unlocked_supply'].append(0)
        
        # Amount while after cliff before vesting end
        else:
            category['unlocked_supply'].append(category['vesting_supply'] / category['duration'])
    
    # 0 after vesting end until coin supply end
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
plt.xticks(np.arange(1, months_list[-1] + 1, step=1)) # Change the number of ticks on x axis. Add 1 to months_list because of tge.

# Print chart
plt.show()         