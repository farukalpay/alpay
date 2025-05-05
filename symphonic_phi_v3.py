#!/usr/bin/env python3
"""
Symphonic φ Identity Engine (Final)
-----------------------------------
Features:
1) Dual node output (public vs. internal)
2) --email-only to show only public addresses in folds/test
3) Resume, Resolve, Graph, Test-Email integrated
4) Collision-resistant with wave fingerprints

CLI usage:
  --generate
  --test
  --iterations N
  --resume NODE
  --resolve NODE
  --graph NODE1 [NODE2 ...]
  --test-email (extended stats in test)
  --email-only (show only public addresses)
  --verbose (debug outputs)
  
Author: Faruk Alpay
ORCID: 0009-0009-2207-6528
Contact: alpay@lightcap.ai
"""

import sys
import argparse
import re

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
            self._resume_from_node(resume_node)
    
    def fold(self, external_input=""):
        """
        Perform one symbolic fold. 
        Returns a dict with:
          - fold_signatures
          - curvature
          - node (internal)
          - public_node (RFC-compliant email)
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
        
        # 6) Compute final node (numeric ID)
        node_id_str, debug_info = self._compute_node_id(new_state, curvature, self.fold_count)
        
        # 7) Build the wave fingerprint for the internal node
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
        
        # Public vs. internal
        public_node_str  = f"n{node_id_str}@alpay.md"
        internal_node_str = f"n{node_id_str}|{wave_fingerprint}@alpay.md"
        
        result = {
            'fold_signatures': new_state,
            'curvature': curvature,
            'node': internal_node_str,     # internal wave-based node
            'public_node': public_node_str,  # plain email
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
        Format: nXXXX|W-<omega>C-<curv>K-<kappa>F-<foldCount>@alpay.md
        """
        if '|' not in node_str:
            return
        
        before_pipe, after_pipe = node_str.split('|', 1)
        if '@alpay.md' in after_pipe:
            after_pipe = after_pipe.replace('@alpay.md', '')
        
        pieces = after_pipe.split('F-')
        if len(pieces) == 2:
            freq_part, fold_str = pieces
            try:
                restored_fold = int(fold_str)
                if restored_fold > 0:
                    self.fold_count = restored_fold
            except:
                pass
    
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
            product_val *= (1 + wave_val)
        
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
        """Fake wave-based permutation sum approach."""
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
# Node Parsing for --graph
# ----------------------------------------------------------------------

def parse_node_for_graph(node_str):
    """
    Parse a node like 'n23442|W-1820C-13K-888F-123@alpay.md'
    Return a dict with:
      numeric_id (int),
      wave_omega (int),
      curv_sum (int),
      kappa_sum (int),
      fold_count (int),
      full_node (original string).
    If parse fails partially, fill missing fields with 0.
    """
    result = {
        'numeric_id': 0,
        'wave_omega': 0,
        'curv_sum': 0,
        'kappa_sum': 0,
        'fold_count': 0,
        'full_node': node_str
    }
    numeric_id = 0
    wave_omega = 0
    curv_sum   = 0
    kappa_sum  = 0
    fold_count = 0
    
    # parse numeric ID after 'n'
    if node_str.startswith('n'):
        after_n = node_str[1:]
        pipe_idx = after_n.find('|')
        if pipe_idx >= 0:
            id_part = after_n[:pipe_idx]
        else:
            # check '@'
            at_idx = after_n.find('@')
            if at_idx >= 0:
                id_part = after_n[:at_idx]
            else:
                id_part = after_n
        try:
            numeric_id = int(id_part)
        except:
            numeric_id = 0
    
    # parse wave part => 'W-..C-..K-..F-..'
    if '|' in node_str:
        parts = node_str.split('|',1)
        wave_part = parts[1]
        if '@alpay.md' in wave_part:
            wave_part = wave_part.replace('@alpay.md','')
        
        # remove leading 'W-'
        if wave_part.startswith('W-'):
            wave_part = wave_part[2:]
        
        c_idx = wave_part.find('C-')
        if c_idx != -1:
            w_str = wave_part[:c_idx]
            try:
                wave_omega = int(w_str)
            except:
                wave_omega = 0
            wave_part = wave_part[c_idx+2:]
        
        k_idx = wave_part.find('K-')
        if k_idx != -1:
            c_str = wave_part[:k_idx]
            try:
                curv_sum = int(c_str)
            except:
                curv_sum = 0
            wave_part = wave_part[k_idx+2:]
        
        f_idx = wave_part.find('F-')
        if f_idx != -1:
            k_str = wave_part[:f_idx]
            try:
                kappa_sum = int(k_str)
            except:
                kappa_sum = 0
            wave_part = wave_part[f_idx+2:]
            try:
                fold_count = int(wave_part)
            except:
                fold_count = 0
    
    result['numeric_id'] = numeric_id
    result['wave_omega'] = wave_omega
    result['curv_sum']   = curv_sum
    result['kappa_sum']  = kappa_sum
    result['fold_count'] = fold_count
    return result


def run_graph(node_list):
    """
    For each pair (i < j) in node_list, parse, compute:
      - ID Δ
      - ω Δ
      - curvature Δ
      - κ Δ
      - fold Δ
      - drift label
    """
    parsed = [parse_node_for_graph(n) for n in node_list]
    
    print("\n=== φ Identity Graph ===")
    for i, nodeA in enumerate(parsed):
        print(f"Node #{i+1}: {nodeA['full_node']}")
    print("-----------------------")
    
    # pairwise
    print("\nPairwise Comparisons:")
    if len(parsed) < 2:
        print("Need at least 2 nodes to compare.")
        return
    
    for i in range(len(parsed)):
        for j in range(i+1, len(parsed)):
            A = parsed[i]
            B = parsed[j]
            
            id_delta = abs(A['numeric_id'] - B['numeric_id'])
            wave_delta = abs(A['wave_omega'] - B['wave_omega'])
            curv_delta = abs(A['curv_sum'] - B['curv_sum'])
            kapp_delta = abs(A['kappa_sum'] - B['kappa_sum'])
            fold_delta = abs(A['fold_count'] - B['fold_count'])
            
            drift = id_delta + wave_delta + curv_delta + kapp_delta + fold_delta
            if drift < 100:
                drift_label = "Minimal"
            elif drift < 1000:
                drift_label = "Moderate"
            else:
                drift_label = "High"
            
            print(f"({i+1} vs {j+1}) => ID Δ:{id_delta}, ω Δ:{wave_delta}, C Δ:{curv_delta}, κ Δ:{kapp_delta}, Fold Δ:{fold_delta} => Drift: {drift_label}")
    
    print("=== End Graph ===")


def run_resolve(node_string):
    """
    Parse the node string: nXXXX|W-<omega>C-<curv>K-<kappa>F-<fold>@alpay.md
    Print identity resolution.
    """
    print("\n=== φ Identity Resolution ===")
    print(f"Node: {node_string}")
    
    data = parse_node_for_graph(node_string)
    numeric_id   = data['numeric_id']
    wave_omega   = data['wave_omega']
    curv_sum     = data['curv_sum']
    kappa_sum    = data['kappa_sum']
    fold_count   = data['fold_count']
    
    # symbolic pressure => wave_omega + curv_sum + kappa_sum
    symbolic_pressure = wave_omega + curv_sum + kappa_sum
    
    if symbolic_pressure < 500:
        growth_rate = "Low"
    elif symbolic_pressure < 3000:
        growth_rate = "Moderate"
    else:
        growth_rate = "High"
    
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


def run_generate(verbose=False, resume=None, email_only=False):
    """Runs a single fold, prints symbolic signatures + final node(s)."""
    phi = SymphonicPhiSystem(verbose=verbose, resume_node=resume)
    res = phi.fold("GEN")
    
    print("\n=== Single Fold Generation ===")
    print(f"Fold Count: {res['fold_count']}")
    
    # Print signatures if not suppressed
    if not email_only:
        print("Signatures:")
        for k in ['tau','omega','delta','epsilon','eta','kappa','zeta']:
            print(f"  {k}: {res['fold_signatures'][k]}")
        print("\nCurvature:")
        for k, v in res['curvature'].items():
            print(f"  {k}: {v}")
    
    # Show final node
    if email_only:
        # Show only public address
        print(f"\nPublic Address => {res['public_node']}")
    else:
        # Show both
        print(f"\nPublic Address  => {res['public_node']}")
        print(f"Internal Node   => {res['node']}")
    
    if verbose and 'debug_info' in res:
        dbg = res['debug_info']
        print("\n--- Symbolic Pressure Breakdown ---")
        for dk, dv in dbg.items():
            print(f" {dk}: {dv}")
    
    print("=== End ===")


def run_test(iterations=10, verbose=False, resume=None, test_email=False, email_only=False):
    """
    Run multiple folds with identical input, checking for collisions.
    If 'test_email' is True, we do extended stats about node formats at the end.
    If 'email_only' is True, we only display public addresses (but collision test uses internal).
    """
    phi = SymphonicPhiSystem(verbose=verbose, resume_node=resume)
    
    print(f"\nTesting φ Identity System over {iterations} iterations...")
    if resume:
        print(f"Resuming from node => {resume}")
    print("-"*70)
    
    # Adjust columns for email_only or verbose
    if verbose:
        header = f"{'Fold':<6} {'Node':<28} {'Curvature':<15} {'digits':<6}"
    else:
        if email_only:
            header = f"{'Fold':<6} {'Public Address':<60}"
        else:
            header = f"{'Fold':<6} {'Node':<60}"
    
    print(header)
    print("-"*70)
    
    generated_nodes = set()
    static_input = "TEST"
    
    email_pattern = re.compile(r"^n\d+@alpay\.md$")
    all_count = 0
    pure_email_count = 0
    
    for i in range(1, iterations+1):
        res = phi.fold(static_input)
        
        # For collision checks, use the internal node
        internal_node = res['node']
        public_node   = res['public_node']
        
        if internal_node in generated_nodes:
            print(f"\nCOLLISION at fold {i}: {internal_node}")
            raise AssertionError("Collision detected — φ has failed!")
        generated_nodes.add(internal_node)
        
        # Email stats
        all_count += 1
        if email_pattern.match(public_node):
            pure_email_count += 1
        
        # Display logic
        if verbose and 'debug_info' in res:
            dbg = res['debug_info']
            curv_str = ",".join(f"{k}:{v}" for k,v in res['curvature'].items())
            # We can show the internal node or public address here
            # If email_only => show public, else show internal
            shown_node = public_node if email_only else internal_node
            print(f"{i:<6} {shown_node:<28} {curv_str:<15} {dbg['digit_count']}")
        else:
            # not verbose
            if email_only:
                # show public only
                shown_node = public_node
            else:
                # show internal
                shown_node = internal_node
            
            print(f"{i:<6} {shown_node:<60}")
    
    print("-"*70)
    print(f"SUCCESS! {iterations} unique nodes generated from identical input.")
    
    if test_email:
        print("\n--- Email Node Stats ---")
        print(f"Total generated: {all_count}")
        print(f"Valid email-only nodes: {pure_email_count}")
        percentage = (pure_email_count / all_count * 100) if all_count else 0
        print(f"Percentage pure email addresses: {percentage:.2f}%")
        print("=== End Email Stats ===")


def main():
    parser = argparse.ArgumentParser(description='Symphonic φ Identity Engine (Final) with Dual Node Output')
    parser.add_argument('--generate', action='store_true', help='Run a single fold, show result')
    parser.add_argument('--test', action='store_true', help='Multiple folds, collision check')
    parser.add_argument('--iterations', type=int, default=10, help='Number of folds in test mode (default=10)')
    parser.add_argument('--resume', type=str, default=None, help='Resume from an internal node (wave-based).')
    parser.add_argument('--resolve', type=str, default=None, help='Resolve a node string into wave details.')
    parser.add_argument('--graph', nargs='+', help='Compare multiple nodes pairwise.')
    parser.add_argument('--test-email', action='store_true', help='Extended email stats when using --test.')
    parser.add_argument('--email-only', action='store_true', help='Show only the public address in output (suppress wave node).')
    parser.add_argument('--verbose', action='store_true', help='Show curvature/pressure debug info')
    
    args = parser.parse_args()
    
    # 1) resolve?
    if args.resolve:
        run_resolve(args.resolve)
        sys.exit(0)
    
    # 2) graph?
    if args.graph:
        run_graph(args.graph)
        sys.exit(0)
    
    # 3) generate/test
    if args.generate:
        run_generate(verbose=args.verbose, resume=args.resume, email_only=args.email_only)
    elif args.test:
        run_test(iterations=args.iterations, 
                 verbose=args.verbose, 
                 resume=args.resume, 
                 test_email=args.test_email,
                 email_only=args.email_only)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
