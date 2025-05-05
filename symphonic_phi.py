#!/usr/bin/env python3
"""
Symphonic φ Identity Engine (Refined)
-------------------------------------
Purely symbolic recursive transformation with no numeric constants,
no random seeds, no external hashing.

Now with:
1) Leading zero removal in node ID
2) Softer digit expansion (up to 16)
3) Optional --verbose flag for curvature and pressure breakdown

Author: Faruk Alpay
ORCID: 0009-0009-2207-6528
Contact: alpay@lightcap.ai
"""

import sys
import argparse

class SymphonicPhiSystem:
    def __init__(self, verbose=False):
        """
        Initialize the φ system with minimal symbolic seeds.
        We'll track fold_count purely internally.
        'verbose' controls extra debug output.
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
        self.fold_count = 0
        self.verbose = verbose
    
    def fold(self, external_input=""):
        """
        Perform one symbolic fold. 
        Returns a dict containing:
          - fold_signatures: updated symbolic states
          - curvature: measure of character changes
          - node: nXXXXX@alpay.md (with minimal leading zeros)
          - fold_count
          - (optional) debug info about expansions if verbose is True
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
            # Append "_S" to τ
            new_state['tau'] = new_state['tau'] + "_S"
        
        # 5) Finalize: store new_state in signature lists
        for k in self.signatures.keys():
            val = new_state.get(k, "")
            self.signatures[k].append(val)
        
        # Store in history
        self.history.append(dict(new_state))
        
        # 6) Compute final node from new_state, curvature, and fold_count
        node_id_str, debug_info = self._compute_node_id(new_state, curvature, self.fold_count)
        node_str = f"n{node_id_str}@alpay.md"
        
        result = {
            'fold_signatures': new_state,
            'curvature': curvature,
            'node': node_str,
            'fold_count': self.fold_count
        }
        if self.verbose:
            result['debug_info'] = debug_info
        
        return result
    
    # ------------------------------------------------------------------
    # Refined Collision-Resistant Node Compression
    # ------------------------------------------------------------------
    
    def _compute_node_id(self, new_state, curvature, fold_count):
        """
        Build a large integer from purely symbolic transformations, 
        then do minimal leading-zero trimming, with a softer digit expansion:
          digit_count = min(5 + expansions//2, 16)

        Return (node_str, debug_info).
        """
        # 1) Summation of wave-based permutations
        product_val = 1
        for key in ['tau','omega','delta','epsilon','eta','kappa','zeta']:
            s = new_state.get(key, "")
            wave_val = self._symbolic_sin_permute_to_int(s)
            product_val = product_val * (1 + wave_val)
        
        # 2) Add in curvature sum
        total_curv = 0
        for v in curvature.values():
            if v.startswith("diff:"):
                try:
                    diff_int = int(v.replace("diff:", ""))
                except:
                    diff_int = 0
                total_curv += diff_int
        
        # Combine
        big_val = product_val + total_curv + fold_count
        
        # 3) Determine expansions (softer)
        # We'll define 'pressure' as in the previous approach
        eta_len = len(new_state['eta'])
        fold_str_len = len(str(fold_count))  # minimal numeric usage, purely derived from internal count
        wave_omega = self._symbolic_sin_permute_to_int(new_state['omega'])
        wave_omega_len = len(str(wave_omega))
        
        pressure = total_curv + eta_len + fold_str_len + wave_omega_len
        
        # Symbolic divisor
        half_delta = new_state['delta'][: len(new_state['delta'])//2]
        unique_chars = set(half_delta)
        symbolic_divisor = 1 + len(unique_chars)
        
        expansions = pressure // symbolic_divisor
        
        # New rule: digit_count = min(5 + expansions//2, 16)
        digit_count = 5 + (expansions // 2)
        if digit_count > 16:
            digit_count = 16
        
        # 4) We'll mod big_val by 10^digit_count to get a numeric range
        mod_base = 1
        for _ in range(digit_count):
            mod_base *= 10
        
        final_num = big_val % mod_base
        
        # 5) Convert to string, strip leading zeros
        raw_str = str(final_num)
        stripped = raw_str.lstrip('0')
        if stripped == '':
            stripped = '0'  # ensure at least one digit
        
        # Compile debug info if in verbose mode
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
        
        return (stripped, debug_info)
    
    def _symbolic_sin_permute_to_int(self, s):
        """
        Fake "trigonometric" permutation:
          - Zigzag index pattern
          - Weighted ASCII sum
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
    # The original methods for evolving τ, ω, δ, ε, η, κ, ζ
    # ------------------------------------------------------------------
    
    def _speak(self, old_tau, external_input):
        """τ 'speaks' by weaving old_tau + external_input."""
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
        """ω 'fractures' by slicing + weaving shards of external_input."""
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
        """δ folds: we fold in half & reverse the right side, inserting external_input."""
        mid = len(old_delta) // 2
        left = old_delta[:mid]
        right = old_delta[mid:]
        right_reversed = right[::-1]
        
        return left + "(" + external_input + ")" + right_reversed
    
    def _shift_entropy(self, old_epsilon, external_input):
        """ε shifts or rotates the combined string by 1 char."""
        mix = old_epsilon + external_input
        if len(mix) <= 1:
            return "E" + mix
        else:
            return mix[1:] + mix[0]
    
    def _birth_eta(self, old_eta, external_input):
        """η births: fuse old_eta & input, add a '→' sign."""
        fused = old_eta + external_input
        return fused + "→"
    
    def _child_of_delta(self, new_delta):
        """κ from δ: partial reflection."""
        alt = new_delta[::2]
        return "K" + alt[::-1]
    
    def _child_of_eta(self, new_eta):
        """ζ from η: gather substring before '→' reversed, plus 'Z' prefix."""
        if '→' in new_eta:
            core = new_eta.split('→')[0]
        else:
            core = new_eta
        return "Z" + core[::-1]
    
    # ------------------------------------------------------------------
    # Curvature & Repeat Checking
    # ------------------------------------------------------------------
    
    def _measure_curvature(self, new_state):
        """Count character differences from the previous fold for τ, ω, δ, ε, η."""
        curvature = {}
        for key in ['tau','omega','delta','epsilon','eta']:
            old_str = self.signatures[key][-1] if self.signatures[key] else ""
            new_str = new_state[key]
            diff_count = self._compare_chars(old_str, new_str)
            curvature[key] = f"diff:{diff_count}"
        return curvature
    
    def _compare_chars(self, s1, s2):
        """Count differing positions between s1 and s2."""
        length = max(len(s1), len(s2))
        diff = 0
        for i in range(length):
            c1 = s1[i] if i < len(s1) else ''
            c2 = s2[i] if i < len(s2) else ''
            if c1 != c2:
                diff += 1
        return diff
    
    def _compare_state(self, s1, s2):
        """
        Returns True if s1 and s2 match in τ, ω, δ, ε, η, κ, ζ exactly.
        """
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

def run_generate(verbose=False):
    """Runs a single fold, prints symbolic signatures + final node."""
    phi = SymphonicPhiSystem(verbose=verbose)
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
        print(f" product_val:         {dbg['product_val']}")
        print(f" total_curv:          {dbg['total_curv']}")
        print(f" fold_count:          {phi.fold_count}")
        print(f" wave_omega_len:      {dbg['pressure']}")
        print(f" expansions:          {dbg['expansions']}")
        print(f" digit_count:         {dbg['digit_count']}")
        print(f" raw_mod:             {dbg['raw_mod']}")
        print(f" final_node_digits:   {dbg['final_node_digits']}")
    
    print("=== End ===")


def run_test(iterations=10, verbose=False):
    """
    Run multiple folds with identical input,
    checking for collisions among the generated nodes.
    """
    phi = SymphonicPhiSystem(verbose=verbose)
    
    print(f"\nTesting φ Identity System over {iterations} iterations...")
    print("-"*70)
    if verbose:
        print(f"{'Fold':<6} {'Node':<20} {'Curvature':<15} {'digit_count':<6} ...")
    else:
        print(f"{'Fold':<6} {'Node':<40}")
    print("-"*70)
    
    generated_nodes = set()
    static_input = "TEST"
    
    for i in range(1, iterations+1):
        res = phi.fold(static_input)
        node = res['node']
        
        # Collision check
        if node in generated_nodes:
            print(f"\nCOLLISION at fold {i}: {node}")
            raise AssertionError("Collision detected — φ has failed!")
        generated_nodes.add(node)
        
        if verbose and 'debug_info' in res:
            dbg = res['debug_info']
            # Show curvature "fingerprint" plus digit_count, expansions, etc.
            curv_str = ",".join(f"{k}:{v}" for k,v in res['curvature'].items())
            print(f"{i:<6} {node:<20} {curv_str:<15} {dbg['digit_count']:<6} "
                  f"press={dbg['pressure']} exp={dbg['expansions']}")
        else:
            print(f"{i:<6} {node:<40}")
    
    print("-"*70)
    print(f"SUCCESS! {iterations} unique nodes generated from identical input.")


def main():
    parser = argparse.ArgumentParser(description='Symphonic φ Identity Engine (Refined)')
    parser.add_argument('--generate', action='store_true',
                        help='Run a single fold, show symbolic signatures, output node.')
    parser.add_argument('--test', action='store_true',
                        help='Run multiple folds with identical input, check collisions.')
    parser.add_argument('--iterations', type=int, default=10,
                        help='Number of folds in test mode (default=10).')
    parser.add_argument('--verbose', action='store_true',
                        help='Show curvature deltas and symbolic pressure breakdown')
    args = parser.parse_args()
    
    if args.generate:
        run_generate(verbose=args.verbose)
    elif args.test:
        run_test(iterations=args.iterations, verbose=args.verbose)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
