---
layout: center
class: bg-gray-900 text-white
---

<div class="flex flex-col items-center justify-center h-full gap-6">
  <h1 class="text-4xl font-bold text-center leading-tight max-w-3xl">
    Mixture of Experts &amp; Long Context:<br/>
    <span class="text-blue-400">Scaling Efficiency to 1M Tokens</span>
  </h1>

  <div class="text-xl text-gray-300 text-center mt-2">
    ACM Class 2026 &nbsp;·&nbsp; CS2916-01 Large Language Models
  </div>

  <div class="text-gray-400 text-lg mt-4">
    Your Name
  </div>

  <div class="text-gray-500 text-sm mt-2">
    April 2026
  </div>
</div>

---
layout: default
class: bg-gray-900 text-white
---

# <span class="text-blue-400">Why MoE + Long Context?</span>

<div class="grid grid-cols-2 gap-8 mt-6">

<div class="bg-gray-800 rounded-xl p-6 border border-blue-500/30">
  <div class="text-blue-400 font-semibold text-lg mb-3">Mixture of Experts (MoE)</div>
  <p class="text-gray-200 leading-relaxed">
    Activates only $k$ of $N_{\text{exp}}$ experts per token — slashes <strong>active FLOPs</strong> without shrinking model capacity.
  </p>
  <div class="mt-4 bg-gray-700/50 rounded-lg p-3 text-sm text-gray-300">
    <span class="text-yellow-400 font-mono">Example:</span> Mixtral activates
    <span class="font-bold text-white">2 of 8</span> experts per token,
    reducing active compute by <span class="text-green-400">~4×</span>.
  </div>
</div>

<div class="bg-gray-800 rounded-xl p-6 border border-purple-500/30">
  <div class="text-purple-400 font-semibold text-lg mb-3">Long Context (LC)</div>
  <p class="text-gray-200 leading-relaxed">
    Extends sequence length $L$ to <strong>128K – 1M tokens</strong>, enabling document-level reasoning and retrieval without chunking.
  </p>
  <div class="mt-4 bg-gray-700/50 rounded-lg p-3 text-sm text-gray-300">
    <span class="text-yellow-400 font-mono">Enables:</span> full-book QA, repo-level code understanding, long-horizon agents.
  </div>
</div>

</div>

<div class="mt-8 text-center text-gray-300 bg-gray-800/60 rounded-xl py-3 px-6 border border-gray-600/40 text-base">
  Together: <span class="text-white font-semibold">capable models that stay compute-efficient at scale</span>
</div>

---
layout: default
class: bg-gray-900 text-white
---

# <span class="text-blue-400">Talk Structure</span>

<div class="grid grid-cols-2 gap-6 mt-4">

<ol class="list-none space-y-3 text-gray-200">
  <li class="flex items-center gap-3">
    <span class="bg-blue-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm flex-shrink-0">1</span>
    <span><strong>Background</strong> <span class="text-gray-400 text-sm ml-1">— 8 min</span></span>
  </li>
  <li class="flex items-center gap-3">
    <span class="bg-blue-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm flex-shrink-0">2</span>
    <span><strong>MoE Architecture</strong> <span class="text-gray-400 text-sm ml-1">— 12 min</span></span>
  </li>
  <li class="flex items-center gap-3">
    <span class="bg-blue-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm flex-shrink-0">3</span>
    <span><strong>Routing Algorithms</strong> <span class="text-gray-400 text-sm ml-1">— 12 min</span></span>
  </li>
  <li class="flex items-center gap-3">
    <span class="bg-purple-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm flex-shrink-0">4</span>
    <span><strong>Long Context Techniques</strong> <span class="text-gray-400 text-sm ml-1">— 12 min</span></span>
  </li>
  <li class="flex items-center gap-3">
    <span class="bg-purple-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm flex-shrink-0">5</span>
    <span><strong>MoE + LC Integration</strong> <span class="text-gray-400 text-sm ml-1">— 15 min</span></span>
  </li>
  <li class="flex items-center gap-3">
    <span class="bg-gray-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm flex-shrink-0">6</span>
    <span><strong>Open Problems</strong> <span class="text-gray-400 text-sm ml-1">— 11 min</span></span>
  </li>
</ol>

<div class="flex items-center justify-center">
  <svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg" class="w-full max-w-md">
    <!-- Background -->
    <rect width="420" height="200" fill="#111827" rx="12"/>

    <!-- Step boxes -->
    <!-- 1: Background -->
    <rect x="10" y="70" width="56" height="36" rx="6" fill="#2563eb" opacity="0.85"/>
    <text x="38" y="84" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Back-</text>
    <text x="38" y="96" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">ground</text>
    <text x="38" y="118" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Inter,sans-serif">8 min</text>

    <!-- Arrow 1→2 -->
    <line x1="66" y1="88" x2="78" y2="88" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arr)"/>

    <!-- 2: MoE Arch -->
    <rect x="78" y="70" width="56" height="36" rx="6" fill="#2563eb" opacity="0.85"/>
    <text x="106" y="84" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">MoE</text>
    <text x="106" y="96" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Arch</text>
    <text x="106" y="118" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Inter,sans-serif">12 min</text>

    <!-- Arrow 2→3 -->
    <line x1="134" y1="88" x2="146" y2="88" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arr)"/>

    <!-- 3: Routing -->
    <rect x="146" y="70" width="56" height="36" rx="6" fill="#2563eb" opacity="0.85"/>
    <text x="174" y="84" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Routing</text>
    <text x="174" y="96" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Algos</text>
    <text x="174" y="118" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Inter,sans-serif">12 min</text>

    <!-- Arrow 3→4 -->
    <line x1="202" y1="88" x2="214" y2="88" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arr)"/>

    <!-- 4: Long Context -->
    <rect x="214" y="70" width="56" height="36" rx="6" fill="#7c3aed" opacity="0.85"/>
    <text x="242" y="84" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Long</text>
    <text x="242" y="96" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Context</text>
    <text x="242" y="118" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Inter,sans-serif">12 min</text>

    <!-- Arrow 4→5 -->
    <line x1="270" y1="88" x2="282" y2="88" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arr)"/>

    <!-- 5: Integration -->
    <rect x="282" y="70" width="56" height="36" rx="6" fill="#7c3aed" opacity="0.85"/>
    <text x="310" y="84" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">MoE+LC</text>
    <text x="310" y="96" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Integr.</text>
    <text x="310" y="118" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Inter,sans-serif">15 min</text>

    <!-- Arrow 5→6 -->
    <line x1="338" y1="88" x2="350" y2="88" stroke="#4b5563" stroke-width="1.5" marker-end="url(#arr)"/>

    <!-- 6: Open Problems -->
    <rect x="350" y="70" width="56" height="36" rx="6" fill="#4b5563" opacity="0.85"/>
    <text x="378" y="84" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Open</text>
    <text x="378" y="96" text-anchor="middle" fill="white" font-size="9" font-family="Inter,sans-serif" font-weight="600">Problems</text>
    <text x="378" y="118" text-anchor="middle" fill="#9ca3af" font-size="8" font-family="Inter,sans-serif">11 min</text>

    <!-- Total label -->
    <text x="210" y="160" text-anchor="middle" fill="#6b7280" font-size="9" font-family="Inter,sans-serif">Total: ~70 minutes</text>

    <!-- Arrow marker def -->
    <defs>
      <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
        <path d="M0,0 L0,6 L6,3 z" fill="#4b5563"/>
      </marker>
    </defs>
  </svg>
</div>

</div>
