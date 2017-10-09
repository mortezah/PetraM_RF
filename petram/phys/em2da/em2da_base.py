import traceback
import numpy as np

from petram.model import Domain, Bdry, Pair
from petram.phys.phys_model import Phys, PhysModule, VectorPhysCoefficient

# define variable for this BC.
from petram.phys.vtable import VtableElement, Vtable
data =  (('Einit', VtableElement('Einit', type='float',
                                  guilabel = 'E(init)',
                                  suffix =('r', 'phi', 'z'),
                                  default = np.array([0,0,0]), 
                                  tip = "initial_E",
                                  chkbox = True)),)
class Einit(VectorPhysCoefficient):
   def EvalValue(self, x):
       v = super(Einit, self).EvalValue(x)
       if self.real:  val = v.real
       else: val =  v.imag
       return val

class EM2Da_Domain(Domain, Phys):
    has_3rd_panel = True    
    vt3  = Vtable(data)   
    def __init__(self, **kwargs):
        super(EM2Da_Domain, self).__init__(**kwargs)
        Phys.__init__(self)
        
    def attribute_set(self, v):
        super(EM2Da_Domain, self).attribute_set(v)
        v['sel_readonly'] = False
        v['sel_index'] = []
        return v
    
    def get_init_coeff(self, engine, real=True, kfes=0):
        if kfes != 0: return
        if not self.use_Einit: return
        
        f_name = self.vt3.make_value_or_expression(self)
        coeff = Einit(3, f_name[0],
                       self.get_root_phys().ind_vars,
                       self._local_ns, self._global_ns,
                       real = real)
        return self.restrict_coeff(coeff, engine, vec = True)

class EM2Da_Bdry(Bdry, Phys):
    has_3rd_panel = True        
    vt3  = Vtable(data)   
    def __init__(self, **kwargs):
        super(EM2Da_Bdry, self).__init__(**kwargs)
        Phys.__init__(self)
        
    def attribute_set(self, v):
        super(EM2Da_Bdry, self).attribute_set(v)
        v['sel_readonly'] = False
        v['sel_index'] = []
        return v

    def get_init_coeff(self, engine, real=True, kfes=0):
        if kfes != 0: return
        if not self.use_Einit: return
        
        f_name = self.vt3.make_value_or_expression(self)
        coeff = Einit(3, f_name[0],
                       self.get_root_phys().ind_vars,
                       self._local_ns, self._global_ns,
                       real = real)
        return self.restrict_coeff(coeff, engine, vec = True)
     
