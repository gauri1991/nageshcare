#!/bin/bash
# Deployment script for pushing approved changes to production
# Usage: ./scripts/deploy.sh

set -e  # Exit on any error

echo "========================================="
echo "  NageshCare Production Deployment"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Pre-deployment checks
echo -e "${YELLOW}Running pre-deployment checks...${NC}"
echo ""

# Check if on main branch
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}ERROR: You must be on 'main' branch to deploy.${NC}"
    echo "Current branch: $CURRENT_BRANCH"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}ERROR: You have uncommitted changes.${NC}"
    echo "Please commit or stash your changes before deploying."
    git status --short
    exit 1
fi

# Run tests if they exist
if [ -d "tests" ] || grep -q "pytest" requirements-dev.txt 2>/dev/null; then
    echo -e "${YELLOW}Running tests...${NC}"
    if command -v pytest &> /dev/null; then
        pytest || {
            echo -e "${RED}Tests failed! Aborting deployment.${NC}"
            exit 1
        }
        echo -e "${GREEN}✓ All tests passed${NC}"
    fi
fi

# Check Python syntax
echo -e "${YELLOW}Checking Python syntax...${NC}"
python -m py_compile manage.py nageshcare_website/*.py || {
    echo -e "${RED}Python syntax errors detected! Aborting deployment.${NC}"
    exit 1
}
echo -e "${GREEN}✓ Python syntax check passed${NC}"

# Update version/tag
echo ""
echo -e "${YELLOW}Creating deployment tag...${NC}"
read -p "Enter version tag (e.g., v1.0.1) or press Enter to skip: " VERSION_TAG

if [ ! -z "$VERSION_TAG" ]; then
    git tag -a "$VERSION_TAG" -m "Production deployment $VERSION_TAG - $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${GREEN}✓ Tag created: $VERSION_TAG${NC}"
fi

# Push to GitHub
echo ""
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push origin main

if [ ! -z "$VERSION_TAG" ]; then
    git push origin "$VERSION_TAG"
fi

echo -e "${GREEN}✓ Code pushed to GitHub${NC}"

# Deployment instructions
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Pre-deployment completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps for cPanel deployment:"
echo ""
echo "1. SSH into your cPanel server"
echo "2. Navigate to your app directory:"
echo "   cd ~/nageshcare"
echo ""
echo "3. Pull the latest changes:"
echo "   git pull origin main"
echo ""
echo "4. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "5. Install/update dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "6. Run migrations:"
echo "   python manage.py migrate"
echo ""
echo "7. Collect static files:"
echo "   python manage.py collectstatic --noinput"
echo ""
echo "8. Restart the Python app in cPanel:"
echo "   - Go to cPanel > Setup Python App"
echo "   - Click 'Restart' button"
echo ""
echo "9. Test the production site:"
echo "   - Check homepage loads correctly"
echo "   - Test CMS admin access"
echo "   - Verify static files are loading"
echo ""
echo -e "${YELLOW}TIP: You can also use ./scripts/update_production.sh on the server${NC}"
echo ""
