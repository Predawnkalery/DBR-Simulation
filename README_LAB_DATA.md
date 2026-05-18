# 🧪 Managing In-House Lab Materials

Welcome to the custom database engine for the DBR & VCSEL Simulator! 

Instead of relying solely on the public RefractiveIndex.info database, this application allows you to define proprietary lab materials, custom optical fits, and raw ellipsometry data. 

You do not need to edit any Python code to add new materials. Simply edit the two configuration files included in this folder: `formulas.yml` and `lab_materials.yml`.

---

## 1. `formulas.yml` (The Math Engine)
This file defines the algebraic equations used to calculate the refractive index ($n$) based on wavelength. 

You can define standard optical dispersion models (like Cauchy or Sellmeier) or create your own custom fits. 

**Available Variables & Math:**
* `wl`: Wavelength in nanometers (nm).
* `wl_um`: Wavelength in micrometers (µm).
* Standard math functions are supported: `sqrt()`, `exp()`, `log()`, `sin()`, `cos()`, and `pi`.

**Example:**
```yaml
# A standard 2-term Cauchy equation
cauchy_standard: "A + B / (wl_um**2) + C / (wl_um**4)"

# A custom linear dispersion fit
linear_fit: "n0 + dn_dwl * wl"
```



## 2. `lab_materials.yml` (The Material Library)

This is where you define the actual materials that will appear in the application's dropdown menus. Materials can be either a **formula** (using coefficients) or **tabulated** (using raw data points).

### Adding a Formula Material

If you have a material that follows an equation defined in `formulas.yml`, use `type: "formula"`. You must provide the `formula_id` and the specific `coefficients` for that equation.

YAML

```
  - name: "Lab PECVD Oxide"
    type: "formula"
    formula_id: "cauchy_standard"
    coefficients:
      A: 1.4580
      B: 0.00354
      C: 0.0
```

### Adding Tabulated Data

If you have raw experimental data (e.g., from an ellipsometer), use `type: "tabulated"`. The engine will automatically perform linear interpolation between your data points.

- Provide data as a list of arrays: `[Wavelength in nm, n, k]`.
    
- _Note: The extinction coefficient (k) is optional. If omitted, it defaults to 0._
    

YAML

```
  - name: "Spin-Coated TiO2 (Sample A)"
    type: "tabulated"
    data:
      - [400, 2.510, 0.002]
      - [500, 2.450, 0.000]
      - [600, 2.390, 0.000]
```
