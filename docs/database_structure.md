# Database Structure

The main database is stored in an sqlite file called `data.sqlite` which stores:

- Boards: All board in the given instance
- Categories: All the categories for each board
- Notes: The notes for all boards
- Settings: The main instance settings

## Table Structures

### Boards

| Name | Type | NN | PK | AI | U | Default |
|-|-|-|-|-|-|-|
| id | INTEGER | X | X | X | - | - |
| name | VARCHAR(30) | X | - | - | - | - |

### Categories

| Name | Type | NN | PK | AI | U | Default |
|-|-|-|-|-|-|-|
| id | INTEGER | X | X | X | - | - |
| name | VARCHAR(30) | X | - | - | - | - |
| board_id | INTEGER | X | - | - | - | - |

### Notes

| Name | Type | NN | PK | AI | U | Default |
|-|-|-|-|-|-|-|
| id | INTEGER | X | X | X | - | - |
| description | VARCHAR(30) | X | - | - | - | - |
| category | INTEGER | X | - | - | - | - |
| tags | JSON | X | - | - | - | - |
| board_id | INTEGER | X | - | - | - | - |

### Settings

| Name | Type | NN | PK | AI | U | Default |
|-|-|-|-|-|-|-|
| setting_name | VARCHAR | X | X | - | - | - |
| setting_value | VARCHAR(64) | X | - | - | - | - |
| setting_type | VARCHAR(16) | X | - | - | - | - |
| setting_display_name | VARCHAR(32) | X | - | - | - | - |
| setting_description | VARCHAR(128) | X | - | - | - | - |
