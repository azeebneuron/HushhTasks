#!/bin/bash
# setup_environment.sh

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting environment setup...${NC}"

# Check if Python 3.8+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo -e "${RED}Error: Python 3.8 or higher is required. Current version: $python_version${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install required packages
echo -e "${YELLOW}Installing required packages...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "${YELLOW}Creating project directories...${NC}"
directories=(
    "config"
    "models/llama"
    "processors"
    "utils"
    "tests/test_data"
    "output/processed"
    "output/comparisons"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    echo "Created directory: $dir"
done

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo "Created .env file. Please update it with your API keys."
fi

echo -e "${GREEN}Environment setup completed successfully!${NC}"