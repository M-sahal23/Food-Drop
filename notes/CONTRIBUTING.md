# Contributing to Django Food Ordering System

Thank you for your interest in contributing to our project! We welcome contributions of all kinds, from bug reports to feature implementations.

## 📋 Code of Conduct

Be respectful, inclusive, and professional in all interactions. Harassment of any kind will not be tolerated.

## 🚀 Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/django-food-ordering.git
cd django-food-ordering
```

### 2. Create Virtual Environment
```bash
python -m venv env1
source env1/bin/activate  # Windows: env1\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dev tools
```

### 4. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## 📝 Development Guidelines

### Code Style
- Follow **PEP 8** standards
- Use **4 spaces** for indentation
- Maximum **79 characters** per line
- Use meaningful variable names
- Add docstrings to functions and classes

### Example:
```python
def calculate_order_total(items, tax_rate=0.08):
    """
    Calculate total price including tax for order items.
    
    Args:
        items (list): List of cart items with prices
        tax_rate (float): Tax rate as decimal (default 0.08)
    
    Returns:
        float: Total price including tax
    """
    subtotal = sum(item.get('price', 0) for item in items)
    tax = subtotal * tax_rate
    return round(subtotal + tax, 2)
```

### Commit Messages
```
✨ Add new food search feature
🐛 Fix cart quantity update bug
🔒 Improve payment security
📚 Update API documentation
🎨 Improve UI responsive design
♻️ Refactor database queries
⚡ Optimize image loading

Format: <emoji> <type>: <description>
- 50 characters or less
- Use imperative mood
- Reference issues when applicable: Fixes #123
```

### Branch Naming
```
feature/user-authentication
bugfix/payment-validation
docs/api-documentation
refactor/database-models
style/css-improvements
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test

# Test specific app
python manage.py test foods

# With verbose output
python manage.py test --verbosity=2

# Generate coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Writing Tests
```python
from django.test import TestCase
from foods.models import FoodItems

class FoodItemsTestCase(TestCase):
    def setUp(self):
        FoodItems.objects.create(
            name="Pizza Margherita",
            price=500,
            rating=4,
            category="PIZZA"
        )
    
    def test_food_creation(self):
        pizza = FoodItems.objects.get(name="Pizza Margherita")
        self.assertEqual(pizza.price, 500)
        self.assertEqual(pizza.category, "PIZZA")
```

## 🔍 Pull Request Process

### 1. Before Submitting
- [ ] Code follows PEP 8 style guide
- [ ] All tests pass locally
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] No console errors or warnings
- [ ] Commit messages are clear

### 2. Create Pull Request
```bash
git push origin feature/your-feature-name
```

### 3. PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123, Related to #456

## Testing Done
Describe testing performed

## Screenshots (if applicable)
Add UI changes screenshots

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
```

### 4. Code Review
- Expect constructive feedback
- Respond to review comments
- Make requested changes
- Request re-review

## 📦 Adding Dependencies

### Python Packages
```bash
# Install package
pip install new-package

# Update requirements
pip freeze > requirements.txt

# In PR, explain why package is needed
```

### Guidelines
- Use stable versions
- Minimize dependencies
- Check for security vulnerabilities
- Get approval before adding

## 🐛 Reporting Bugs

### Create Issue with Details
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows/Mac/Linux
- Python: 3.8/3.9/3.10
- Django: 5.2
- Browser: Chrome/Firefox

## Screenshots/Logs
Include error messages
```

## 💡 Feature Requests

```markdown
## Feature Description
Clear description of feature

## Use Case
Why this feature is needed

## Implementation Ideas
How it could work

## Related Issues
Link to related issues
```

## 📚 Documentation

### Adding Docs
1. Update relevant `.md` files
2. Add docstrings to code
3. Update API documentation
4. Include examples

### Documentation Format
```python
"""
Module docstring explaining purpose.

Classes:
    FoodItems: Represents food items in catalog
    
Functions:
    get_food_by_category: Retrieve foods by category
"""
```

## 🔐 Security

### Report Security Issues
- **DO NOT** create public issue
- Email: security@example.com
- Include details and steps
- Allow time for fix before disclosure

### Security Guidelines
- Never commit secrets (.env files)
- Validate all user inputs
- Use parameterized queries (ORM)
- Implement CSRF protection
- Use HTTPS in production

## 💻 Local Development Workflow

### Make Changes
```bash
# Create branch
git checkout -b feature/my-feature

# Make changes
# Test locally
python manage.py runserver

# Run tests
python manage.py test
```

### Commit & Push
```bash
git add .
git commit -m "✨ Add amazing feature"
git push origin feature/my-feature
```

### Create Pull Request
- Go to GitHub
- Create PR from your branch
- Fill out PR template
- Request reviewers

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Recognized in README

## 📞 Getting Help

- 💬 Open issue for questions
- 🔗 Start discussion
- 📧 Email maintainers
- 💭 Join Discord/Slack

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Git Guide](https://git-scm.com/docs)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🎉**

Questions? Open an issue or contact the maintainers.
