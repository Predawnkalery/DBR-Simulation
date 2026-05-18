import numpy as np

class LabMaterial:
    def __init__(self, yaml_node, formulas_dict):
        self.yaml_node = yaml_node
        self.name = yaml_node.get('name', 'Unknown Lab Material')
        self.type = yaml_node.get('type', 'tabulated') 
        
        # Store the master list of formulas
        self.formulas = formulas_dict

    def get_refractive_index(self, wl_nm):
        if self.type == 'tabulated':
            # Linear Interpolation for raw data
            data = np.array(self.yaml_node['data'])
            wls = data[:, 0]
            ns = data[:, 1]
            return float(np.interp(wl_nm, wls, ns))

        elif self.type == 'formula':
            formula_id = self.yaml_node.get('formula_id')
            
            # Fetch the equation string from the formulas dictionary
            eq = self.formulas.get(formula_id)
            if not eq:
                print(f"Error: Formula ID '{formula_id}' not found in formulas.yml")
                return 1.0

            coeffs = self.yaml_node.get('coefficients', {})

            variables = {
                'wl': float(wl_nm),
                'wl_um': float(wl_nm) / 1000.0
            }
            variables.update(coeffs)

            safe_math = {
                'sqrt': np.sqrt, 'exp': np.exp, 'log': np.log, 
                'sin': np.sin, 'cos': np.cos, 'pi': np.pi
            }

            try:
                n_val = eval(eq, {"__builtins__": {}}, {**safe_math, **variables})
                return float(n_val)
            except Exception as e:
                print(f"Math error in {self.name} formula: {e}")
                return 1.0

        return 1.0

    def get_extinction_coefficient(self, wl_nm):
        if self.type == 'tabulated':
            data = np.array(self.yaml_node['data'])
            if data.shape[1] > 2:
                wls = data[:, 0]
                ks = data[:, 2]
                return float(np.interp(wl_nm, wls, ks))
        return 0.0