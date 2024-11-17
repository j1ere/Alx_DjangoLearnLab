# Permissions and Groups Setup

## Custom Permissions
- `Book` model includes the following permissions:
  - `can_view`: Can view books.
  - `can_create`: Can create books.
  - `can_edit`: Can edit books.
  - `can_delete`: Can delete books.

## Groups
- **Viewers**: Can only view books.
- **Editors**: Can view, create, and edit books.
- **Admins**: Can perform all actions on books.

## View Protection
- `@permission_required` decorator is used to enforce permissions in views.
  - Example: `@permission_required('myapp.can_edit', raise_exception=True)`

## Automated Setup
- Use the `create_groups_and_permissions` management command to create default groups and permissions.
  - Run: `python manage.py create_groups_and_permissions`

## Testing
- Create test users and assign them to groups via the Django admin interface.
- Log in as these users to verify permissions are enforced.

