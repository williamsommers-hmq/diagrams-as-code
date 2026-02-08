import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hivemq_theme import HiveMQPalette

# This will now automatically create your /icons/ folder and icons.csv if missing
palette = HiveMQPalette('icons.csv')
