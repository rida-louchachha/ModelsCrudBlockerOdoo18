# 🛡️ Odoo Model Operation Blocker

This Odoo 18.0 custom module allows administrators to **block specific operations (create, write, delete)** on any Odoo model via a backend interface. It is ideal for safeguarding sensitive models like products, categories, or user-defined models from accidental changes in a production environment.

---

## 📦 Module Information

| Key        | Value                              |
|------------|-------------------------------------|
| Name       | Models Operation Blocker            |
| Version    | 1.0                                 |
| Category   | Tools                               |
| Author     | Rida Louchachha                     |
| License    | LGPL-3                              |
| Website    | –                                   |
| Compatible | Odoo 18.0                           |
| Depends    | `base`                              |

---

## 🚀 Features

- 🔒 Block **Create**, **Write**, or **Delete** operations on any model.
- ⚙️ Easily configurable from the backend via **Paramétrage**.
- 🔁 Dynamic and reversible without code changes.
- 🔍 View and manage blocked models from a simple UI.
- 🧩 No need to modify existing models — works by dynamically patching ORM operations.

---

## 🖥️ How It Works

The module hooks into Odoo's model registry and dynamically **overrides the `create`, `write`, and `unlink` methods** based on user-defined rules stored in the `model.block.config` model.

If an operation is blocked, users will receive a friendly warning like:

> ❌ The `create` operation on model `product.template` is not allowed from the Odoo interface.  
> ✅ If you want to allow this action, update it Using API OR settings.

---

## 🛠️ Configuration

1. **Install the module**
2. Navigate to **Paramétrage → Model Operation Blocker**
3. Click **Create** and:
   - Choose a model (e.g., `product.template`)
   - Select which operations to block: Create, Write, Delete
4. Save — the changes apply instantly!

---

## 🗃️ Technical Details

- Custom model: `model.block.config`
- Fields:
  - `model_id` – Target model to block
  - `block_create`, `block_write`, `block_unlink` – Boolean flags
- All changes are applied via the function `patch_model_operations(env)` which dynamically injects blocking logic.

---

## 🔒 Security

- Includes appropriate access rights in `ir.model.access.csv`
- Only administrators or users with technical rights should configure blocking rules

---

## 📂 File Structure

models_crud_blocker/
├── models/
│ ├── blocker.py # Patching logic
│ ├── config.py # Model config logic
├── views/
│ └── config_view.xml # Backend form/tree views
├── data/
│ └── model_block_config_data.xml
├── security/
│ └── ir.model.access.csv
├── static/
│ └── description/icon.png
├── manifest.py


---

## 📝 License

This module is licensed under the **LGPL-3** license.

---

## 🙋 Author

**Rida Louchachha**  
Odoo Developer | Python developer  
Email: ridalouchachha2580@gmail.com

---
