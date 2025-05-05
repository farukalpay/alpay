#!/usr/bin/env python3
"""
Symphonic φ Identity Engine with Self-Continuing Resume + Resolver
------------------------------------------------------------------
1. Pure symbolic recursion for fold generation.
2. Collision-resistant node creation with dynamic digit expansion.
3. Self-contained wave-based resume (via --resume).
4. NEW: --resolve NODE_STRING to parse and analyze a node's identity.

CLI commands:
  --generate             => single fold, show result
  --test                 => multiple folds with identical input, check collisions
  --iterations N         => how many folds in test mode
  --verbose              => show curvature/pressure debug
  --resume NODE_STRING   => parse node to re-init system, continue folding
  --resolve NODE_STRING  => parse node, show symbolic stats (no folding)

Author: Faruk Alpay
ORCID: 0009-0009-2207-6528
Contact: alpay@lightcap.ai
"""
#!/usr/bin/env python3
"""
Symphonic φ Identity Engine with Self-Continuing Resume + Resolver
------------------------------------------------------------------
1. Pure symbolic recursion for fold generation.
2. Collision-resistant node creation with dynamic digit expansion.
3. Self-contained wave-based resume (via --resume).
4. NEW: --resolve NODE_STRING to parse and analyze a node's identity.

CLI commands:
  --generate             => single fold, show result
  --test                 => multiple folds with identical input, check collisions
  --iterations N         => how many folds in test mode
  --verbose              => show curvature/pressure debug
  --resume NODE_STRING   => parse node to re-init system, continue folding
  --resolve NODE_STRING  => parse node, show symbolic stats (no folding)
"""

import sys
import argparse


class SymphonicPhiSystem:
    def __init__(self, 
                 verbose=False, 
                 resume_node=None):
        """
        Initialize the φ system with minimal seeds, 
        OR parse 'resume_node' to re-initialize fold_count + wave frequencies.
        """
        self.signatures = {
            'tau': ['τ'],      # Let τ "speak"
            'omega': ['ω'],    # Let ω "fracture"
            'delta': ['δ'],    # Let δ fold into κ
            'epsilon': ['ε'],  # Track "entropy"
            'eta': ['η'],      # Let η birth ζ
            'kappa': [],
            'zeta': []
        }
        self.history = []
        
        # We'll have an internal fold_count that we *may* set from the resume node
        self.fold_count = 0
        self.verbose = verbose
        
        if resume_node:
            # Attempt to parse node to restore system
            self._resume_from_node(resume_node)
    
    def fold(self, external_input=""):
        """
        Perform one symbolic fold. 
        Returns a dict:
          - fold_signatures
          - curvature
          - node (nXXXX|wave@alpay.md)
          - fold_count
        """
        self.fold_count += 1
        
        new_state = {}
        # 1) Evolve each main signature
        new_state['tau']     = self._speak(self.signatures['tau'][-1], external_input)
        new_state['omega']   = self._fracture(self.signatures['omega'][-1], external_input)
        new_state['delta']   = self._fold_delta(self.signatures['delta'][-1], external_input)
        new_state['epsilon'] = self._shift_entropy(self.signatures['epsilon'][-1], external_input)
        new_state['eta']     = self._birth_eta(self.signatures['eta'][-1], external_input)
        
        # 2) δ -> κ, η -> ζ
        new_state['kappa'] = self._child_of_delta(new_state['delta'])
        new_state['zeta']  = self._child_of_eta(new_state['eta'])
        
        # 3) Measure curvature
        curvature = self._measure_curvature(new_state)
        
        # 4) Check if new_state is identical to any prior fold => break symmetry
        if any(self._compare_state(new_state, old) for old in self.history):
            new_state['tau'] = new_state['tau'] + "_S"
        
        # 5) Store new_state
        for k in self.signatures.keys():
            val = new_state.get(k, "")
            self.signatures[k].append(val)
        
        self.history.append(dict(new_state))
        
        # 6) Compute final node
        node_id_str, debug_info = self._compute_node_id(new_state, curvature, self.fold_count)
        
        # 7) Build a "waveform fingerprint" appended after a pipe
        wave_omega = self._symbolic_sin_permute_to_int(new_state['omega'])
        wave_kappa = self._symbolic_sin_permute_to_int(new_state['kappa'])
        total_curv = 0
        for v in curvature.values():
            if v.startswith("diff:"):
                try:
                    diff_int = int(v.replace("diff:", ""))
                except:
                    diff_int = 0
                total_curv += diff_int
        
        wave_fingerprint = f"W-{wave_omega}C-{total_curv}K-{wave_kappa}F-{self.fold_count}"
        
        final_node_str = f"n{node_id_str}|{wave_fingerprint}@alpay.md"
        
        result = {
            'fold_signatures': new_state,
            'curvature': curvature,
            'node': final_node_str,
            'fold_count': self.fold_count
        }
        if self.verbose:
            result['debug_info'] = debug_info
        
        return result
    
    # ------------------------------------------------------------------
    # "Resume" logic
    # ------------------------------------------------------------------
    
    def _resume_from_node(self, node_str):
        """
        Parse node_str to set approximate or exact fold_count 
        and optionally re-init wave states.
        Format: nXXXXXXXX|W-<omega>C-<curv>K-<kappa>F-<foldCount>@alpay.md
        """
        if '|' not in node_str:
            return
        
        before_pipe, after_pipe = node_str.split('|', 1)
        if '@alpay.md' in after_pipe:
            after_pipe = after_pipe.replace('@alpay.md', '')
        
        # Now after_pipe might be W-999C-10K-50F-123
        # We'll parse out F- foldCount
        pieces = after_pipe.split('F-')
        if len(pieces) == 2:
            freq_part, fold_str = pieces
            try:
                restored_fold = int(fold_str)
                if restored_fold > 0:
                    self.fold_count = restored_fold
            except:
                pass
            
            # freq_part might be 'W-999C-10K-50'
            # We could parse wave sums to reinit states, if desired.
    
    # ------------------------------------------------------------------
    # Node ID logic
    # ------------------------------------------------------------------
    
    def _compute_node_id(self, new_state, curvature, fold_count):
        """
        Build an integer from wave-based permutations, curvature, fold_count,
        do softer digit expansions, remove leading zeros.
        """
        # 1) Summation of wave permutations
        product_val = 1
        for key in ['tau','omega','delta','epsilon','eta','kappa','zeta']:
            s = new_state.get(key, "")
            wave_val = self._symbolic_sin_permute_to_int(s)
            product_val = product_val * (1 + wave_val)
        
        # 2) curvature sum
        total_curv = 0
        for v in curvature.values():
            if v.startswith("diff:"):
                try:
                    diff_int = int(v.replace("diff:", ""))
                except:
                    diff_int = 0
                total_curv += diff_int
        
        big_val = product_val + total_curv + fold_count
        
        # 3) expansions
        eta_len = len(new_state['eta'])
        wave_omega = self._symbolic_sin_permute_to_int(new_state['omega'])
        wave_omega_len = len(str(wave_omega))
        fold_str_len = len(str(fold_count))
        
        pressure = total_curv + eta_len + wave_omega_len + fold_str_len
        
        half_delta = new_state['delta'][: len(new_state['delta'])//2]
        unique_chars = set(half_delta)
        symbolic_divisor = 1 + len(unique_chars)
        
        expansions = pressure // symbolic_divisor
        digit_count = 5 + (expansions // 2)
        if digit_count > 16:
            digit_count = 16
        
        mod_base = 1
        for _ in range(digit_count):
            mod_base *= 10
        
        final_num = big_val % mod_base
        
        # remove leading zeros
        raw_str = str(final_num)
        stripped = raw_str.lstrip('0')
        if stripped == '':
            stripped = '0'
        
        debug_info = {
            'big_val': str(big_val),
            'product_val': str(product_val),
            'total_curv': str(total_curv),
            'pressure': str(pressure),
            'symbolic_divisor': str(symbolic_divisor),
            'expansions': str(expansions),
            'digit_count': str(digit_count),
            'raw_mod': raw_str,
            'final_node_digits': stripped
        }
        
        return stripped, debug_info
    
    def _symbolic_sin_permute_to_int(self, s):
        """
        The fake "wave-based" permutation sum approach.
        """
        if not s:
            return 0
        
        indices = []
        i = 0
        step = 1
        visited = set()
        while i >= 0 and i < len(s):
            if i in visited:
                break
            visited.add(i)
            indices.append(i)
            i += step
            step = -step
        
        remaining = [x for x in range(len(s)) if x not in visited]
        indices.extend(remaining)
        
        total = 0
        for pos, idx in enumerate(indices):
            ch = s[idx]
            total += ord(ch) * (pos + 1)
        return total
    
    # ------------------------------------------------------------------
    # Evolving τ, ω, δ, ε, η, κ, ζ
    # ------------------------------------------------------------------
    
    def _speak(self, old_tau, external_input):
        combined = []
        a = list(old_tau)
        b = list(external_input)
        while a or b:
            if a:
                combined.append(a.pop(0))
            if b:
                combined.append(b.pop(0))
        return "T" + "".join(combined)
    
    def _fracture(self, old_omega, external_input):
        half = len(old_omega) // 2
        part1 = old_omega[:half]
        part2 = old_omega[half:]
        cracked = part1 + "|" + part2
        
        shards = []
        c = list(external_input)
        d = list(cracked)
        while c or d:
            if d:
                shards.append(d.pop(0))
            if c:
                shards.append('-'+c.pop(0)+'-')
        return "".join(shards)
    
    def _fold_delta(self, old_delta, external_input):
        mid = len(old_delta) // 2
        left = old_delta[:mid]
        right = old_delta[mid:]
        right_reversed = right[::-1]
        return left + "(" + external_input + ")" + right_reversed
    
    def _shift_entropy(self, old_epsilon, external_input):
        mix = old_epsilon + external_input
        if len(mix) <= 1:
            return "E" + mix
        else:
            return mix[1:] + mix[0]
    
    def _birth_eta(self, old_eta, external_input):
        fused = old_eta + external_input
        return fused + "→"
    
    def _child_of_delta(self, new_delta):
        alt = new_delta[::2]
        return "K" + alt[::-1]
    
    def _child_of_eta(self, new_eta):
        if '→' in new_eta:
            core = new_eta.split('→')[0]
        else:
            core = new_eta
        return "Z" + core[::-1]
    
    # ------------------------------------------------------------------
    # Curvature & Repeat Checking
    # ------------------------------------------------------------------
    
    def _measure_curvature(self, new_state):
        curvature = {}
        for key in ['tau','omega','delta','epsilon','eta']:
            old_str = self.signatures[key][-1] if self.signatures[key] else ""
            new_str = new_state[key]
            diff_count = self._compare_chars(old_str, new_str)
            curvature[key] = f"diff:{diff_count}"
        return curvature
    
    def _compare_chars(self, s1, s2):
        length = max(len(s1), len(s2))
        diff = 0
        for i in range(length):
            c1 = s1[i] if i < len(s1) else ''
            c2 = s2[i] if i < len(s2) else ''
            if c1 != c2:
                diff += 1
        return diff
    
    def _compare_state(self, s1, s2):
        main_keys = ['tau','omega','delta','epsilon','eta','kappa','zeta']
        for k in main_keys:
            if k not in s1 or k not in s2:
                return False
            if s1[k] != s2[k]:
                return False
        return True


# ----------------------------------------------------------------------
# CLI Entry Points
# ----------------------------------------------------------------------

def run_generate(verbose=False, resume=None):
    """Runs a single fold, prints symbolic signatures + final node."""
    phi = SymphonicPhiSystem(verbose=verbose, resume_node=resume)
    result = phi.fold("GEN")  # Example input
    print("\n=== Single Fold Generation ===")
    print(f"Fold Count: {result['fold_count']}")
    print("Signatures:")
    for k in ['tau','omega','delta','epsilon','eta','kappa','zeta']:
        print(f"  {k}: {result['fold_signatures'][k]}")
    print("\nCurvature:")
    for k, v in result['curvature'].items():
        print(f"  {k}: {v}")
    
    print(f"\nFinal Node => {result['node']}")
    
    if verbose and 'debug_info' in result:
        dbg = result['debug_info']
        print("\n--- Symbolic Pressure Breakdown ---")
        for dk, dv in dbg.items():
            print(f" {dk}: {dv}")
    
    print("=== End ===")


def run_test(iterations=10, verbose=False, resume=None):
    """
    Run multiple folds with identical input,
    checking for collisions. 
    If 'resume' is provided, we parse that node first.
    """
    phi = SymphonicPhiSystem(verbose=verbose, resume_node=resume)
    
    print(f"\nTesting φ Identity System over {iterations} iterations...")
    if resume:
        print(f"Resuming from node => {resume}")
    print("-"*70)
    if verbose:
        print(f"{'Fold':<6} {'Node':<28} {'Curvature':<15} {'digits':<6}")
    else:
        print(f"{'Fold':<6} {'Node':<60}")
    print("-"*70)
    
    generated_nodes = set()
    static_input = "TEST"
    
    for i in range(1, iterations+1):
        res = phi.fold(static_input)
        node = res['node']
        
        if node in generated_nodes:
            print(f"\nCOLLISION at fold {i}: {node}")
            raise AssertionError("Collision detected — φ has failed!")
        generated_nodes.add(node)
        
        if verbose and 'debug_info' in res:
            dbg = res['debug_info']
            curv_str = ",".join(f"{k}:{v}" for k,v in res['curvature'].items())
            print(f"{i:<6} {node:<28} {curv_str:<15} {dbg['digit_count']}")
        else:
            print(f"{i:<6} {node:<60}")
    
    print("-"*70)
    print(f"SUCCESS! {iterations} unique nodes generated from identical input.")


def run_resolve(node_string):
    """
    Parse the node string of the form:
      nXXXXX|W-<omega>C-<curv>K-<kappa>F-<fold>@alpay.md
    and print out the identity resolution.

    Output includes:
      - numeric ID
      - fold count
      - ω wave sum
      - curvature sum
      - κ wave sum
      - symbolic pressure
      - expected growth rate
      - final identity statement
    """
    print("\n=== φ Identity Resolution ===")
    print(f"Node: {node_string}")
    
    # 1) Extract numeric ID => 'nXXXX'
    #    We'll split on '|'
    numeric_id = ""
    wave_part = ""
    if '|' in node_string:
        left, right = node_string.split('|', 1)
        # left might be nXXXX
        if left.startswith('n'):
            numeric_id = left[1:]  # skip 'n'
        # right might be W-1820C-10K-888F-123@alpay.md
        if '@alpay.md' in right:
            right = right.replace('@alpay.md', '')
        wave_part = right
    else:
        # fallback: if we have no '|', it might just be nXXXX@alpay.md
        # minimal parse
        if node_string.startswith('n'):
            # strip possible domain part
            parts = node_string.split('@',1)
            numeric_id = parts[0][1:] if len(parts)>0 else ""
    
    # parse wave_part => W-<omega>C-<curv>K-<kappa>F-<fold>
    # We'll attempt to parse with a simple approach
    # default: wave_omega=0, curv=0, kappa=0, folds=0
    wave_omega = 0
    curv_sum = 0
    kappa_sum = 0
    fold_count = 0
    
    # Example wave_part: "W-1820C-10K-888F-123"
    # We'll do stepwise:
    #  1) split by 'W-', 'C-', 'K-', 'F-'
    # or we can do a simpler approach by scanning.
    # Let's just do naive scanning with .split('W-') etc.
    
    # If wave_part is empty, we'll skip
    if wave_part:
        # remove leading 'W-'
        if wave_part.startswith('W-'):
            wave_part = wave_part[2:]  # remove 'W-'
        
        # Now wave_part might start with e.g. "1820C-10K-888F-123"
        # We'll find 'C-'
        c_idx = wave_part.find('C-')
        if c_idx != -1:
            w_str = wave_part[:c_idx]
            wave_part = wave_part[c_idx+2:]
            try:
                wave_omega = int(w_str)
            except:
                wave_omega = 0
        
        # wave_part might now be "10K-888F-123"
        k_idx = wave_part.find('K-')
        if k_idx != -1:
            c_str = wave_part[:k_idx]
            wave_part = wave_part[k_idx+2:]
            try:
                curv_sum = int(c_str)
            except:
                curv_sum = 0
        
        # wave_part might now be "888F-123"
        f_idx = wave_part.find('F-')
        if f_idx != -1:
            k_str = wave_part[:f_idx]
            wave_part = wave_part[f_idx+2:]
            try:
                kappa_sum = int(k_str)
            except:
                kappa_sum = 0
            
            # wave_part might now be '123'
            try:
                fold_count = int(wave_part)
            except:
                fold_count = 0
    
    # Now we have numeric_id, wave_omega, curv_sum, kappa_sum, fold_count
    # 2) Symbolic pressure => wave_omega + curv_sum + kappa_sum
    symbolic_pressure = wave_omega + curv_sum + kappa_sum
    
    # 3) Estimate growth rate:
    #    We'll define a naive threshold
    if symbolic_pressure < 500:
        growth_rate = "Low"
    elif symbolic_pressure < 3000:
        growth_rate = "Moderate"
    else:
        growth_rate = "High"
    
    # 4) Print results
    print(f"Numeric ID     : {numeric_id}")
    print(f"Fold Count     : {fold_count}")
    print(f"ω Waveform     : {wave_omega}")
    print(f"Curvature Sum  : {curv_sum}")
    print(f"κ Symbolic Sum : {kappa_sum}")
    print("")
    print(f"→ Symbolic Pressure: {symbolic_pressure}")
    print(f"→ Expected Growth Rate: {growth_rate}")
    print("→ Identity: Recursively Emergent")
    print("=== End Resolution ===")


def main():
    parser = argparse.ArgumentParser(description='Symphonic φ Identity Engine with Resume + Resolver')
    parser.add_argument('--generate', action='store_true',
                        help='Run a single fold, show symbolic signatures, output node.')
    parser.add_argument('--test', action='store_true',
                        help='Run multiple folds with identical input, check collisions.')
    parser.add_argument('--iterations', type=int, default=10,
                        help='Number of folds in test mode (default=10).')
    parser.add_argument('--verbose', action='store_true',
                        help='Show curvature deltas and symbolic pressure breakdown')
    parser.add_argument('--resume', type=str, default=None,
                        help='A node string to parse for resuming the system state.')
    parser.add_argument('--resolve', type=str, default=None,
                        help='Analyze a given node string (no folding).')
    
    args = parser.parse_args()
    
    # If --resolve is given, do that and exit
    if args.resolve:
        run_resolve(args.resolve)
        sys.exit(0)
    
    if args.generate:
        run_generate(verbose=args.verbose, resume=args.resume)
    elif args.test:
        run_test(iterations=args.iterations, verbose=args.verbose, resume=args.resume)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
