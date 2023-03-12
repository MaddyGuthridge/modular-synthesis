
# Generating waveforms
# ====================

# How many samples to generate
SAMPLE_LENGTH = 24_000
# The frequency of the samples in the waveform
SAMPLE_RATE = 24_000

# Printing waveforms
# ==================

# How tall to make the waveform
WAVE_HEIGHT = 10
# What to print where there is a wave
WAVE_CHAR = '█'
# What to print where there isn't a wave
SPACE_CHAR = ' '

# Type aliases
# ============

# Waveform
Waveform = list[float]
