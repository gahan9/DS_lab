---


---

<h1 id="practical-3"><a href="https://github.com/gahan9/DS_lab/blob/master/practical_3.md">Practical 3</a></h1>
<blockquote>
<p>Implementation of B+ Tree Indexing for Database query processing<br>
Input-output for Select Query on exact Match, Range Query, Insert , delete Query.<br>
Analysis report</p>
</blockquote>
<h2 id="implementation">Implementation</h2>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment">#!usr/bin/python3</span>
<span class="token comment"># coding=utf-8</span>
<span class="token triple-quoted-string string">"""
some terminology of python:
_var =&gt; (convention only) underscore prefix is just a hint to programmer that a variable or method starting with a single underscore is intended for internal use
var_ =&gt; (convention only) to brake name conflict
__var =&gt; “dunders” (name mangling) rewrite the attribute name in order to avoid naming conflicts in subclasses.
            interpreter changes the name of the variable in a way that makes it harder to create collisions when the class is extended later.
"""</span>

<span class="token keyword">import</span> math
<span class="token keyword">import</span> logging
<span class="token keyword">import</span> os
<span class="token keyword">import</span> random
<span class="token keyword">from</span> datetime <span class="token keyword">import</span> datetime
<span class="token keyword">from</span> bisect <span class="token keyword">import</span> bisect_right<span class="token punctuation">,</span> bisect_left
<span class="token keyword">from</span> collections <span class="token keyword">import</span> deque

__author__ <span class="token operator">=</span> <span class="token string">"Gahan Saraiya"</span>
DEBUG <span class="token operator">=</span> <span class="token boolean">False</span>
LOG_DIR <span class="token operator">=</span> <span class="token string">"."</span>
logger <span class="token operator">=</span> logging<span class="token punctuation">.</span>getLogger<span class="token punctuation">(</span><span class="token string">'bPlusTree'</span><span class="token punctuation">)</span>
logging<span class="token punctuation">.</span>basicConfig<span class="token punctuation">(</span>level<span class="token operator">=</span>logging<span class="token punctuation">.</span>DEBUG<span class="token punctuation">,</span>
                    <span class="token builtin">format</span><span class="token operator">=</span><span class="token string">'%(asctime)s [%(name)-8s - %(levelname)s]: %(message)s'</span><span class="token punctuation">,</span>
                    datefmt<span class="token operator">=</span><span class="token string">'[%Y-%d-%m_%H.%M.%S]'</span><span class="token punctuation">,</span>
                    filename<span class="token operator">=</span>os<span class="token punctuation">.</span>path<span class="token punctuation">.</span>join<span class="token punctuation">(</span>LOG_DIR<span class="token punctuation">,</span> <span class="token string">'b_plus_tree.log'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                    filemode<span class="token operator">=</span><span class="token string">'w'</span><span class="token punctuation">)</span>
ch <span class="token operator">=</span> logging<span class="token punctuation">.</span>StreamHandler<span class="token punctuation">(</span><span class="token punctuation">)</span>  <span class="token comment"># create console handler with a higher log level</span>
ch<span class="token punctuation">.</span>setLevel<span class="token punctuation">(</span>logging<span class="token punctuation">.</span>DEBUG<span class="token punctuation">)</span>
<span class="token comment"># create formatter and add it to the handlers</span>
formatter <span class="token operator">=</span> logging<span class="token punctuation">.</span>Formatter<span class="token punctuation">(</span><span class="token string">'%(asctime)s [%(name)-8s - %(levelname)s]: %(message)s'</span><span class="token punctuation">)</span>
ch<span class="token punctuation">.</span>setFormatter<span class="token punctuation">(</span>formatter<span class="token punctuation">)</span>
<span class="token comment"># add the handlers to the logger</span>
logger<span class="token punctuation">.</span>addHandler<span class="token punctuation">(</span>ch<span class="token punctuation">)</span>


<span class="token keyword">def</span> <span class="token function">log</span><span class="token punctuation">(</span><span class="token operator">*</span>msg<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">if</span> DEBUG<span class="token punctuation">:</span>
        logger<span class="token punctuation">.</span>debug<span class="token punctuation">(</span>msg<span class="token punctuation">)</span>
    <span class="token keyword">else</span><span class="token punctuation">:</span>
        <span class="token keyword">pass</span>


<span class="token keyword">class</span> <span class="token class-name">InternalNode</span><span class="token punctuation">(</span><span class="token builtin">object</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">"""
    Class : B+ Tree Internal Node
    represents internal (non-leaf) node in B+ tree
    """</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> degree<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""
        initialize B tree node
        :param degree: specify degree of btree  # default degree set to 4
        """</span>
        self<span class="token punctuation">.</span>degree <span class="token operator">=</span> degree
        self<span class="token punctuation">.</span>keys <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>  <span class="token comment"># store keys/data values</span>
        self<span class="token punctuation">.</span>children <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>  <span class="token comment"># store child nodes (list of instances of BtreeNode); empty list if node is leaf node</span>
        self<span class="token punctuation">.</span>parent <span class="token operator">=</span> <span class="token boolean">None</span>

    <span class="token keyword">def</span> <span class="token function">__repr__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token string">" | "</span><span class="token punctuation">.</span>join<span class="token punctuation">(</span><span class="token builtin">map</span><span class="token punctuation">(</span><span class="token builtin">str</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span>keys<span class="token punctuation">)</span><span class="token punctuation">)</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_leaf</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token boolean">False</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">total_keys</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token builtin">len</span><span class="token punctuation">(</span>self<span class="token punctuation">.</span>keys<span class="token punctuation">)</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_balanced</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token comment"># return False if total keys exceeds max accommodated keys (degree - 1)</span>
        <span class="token keyword">return</span> self<span class="token punctuation">.</span>total_keys <span class="token operator">&lt;=</span> self<span class="token punctuation">.</span>degree <span class="token operator">-</span> <span class="token number">1</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_full</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> self<span class="token punctuation">.</span>total_keys <span class="token operator">&gt;=</span> self<span class="token punctuation">.</span>degree

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_empty</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> self<span class="token punctuation">.</span>total_keys <span class="token operator">&lt;</span> <span class="token punctuation">(</span>self<span class="token punctuation">.</span>degree <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">)</span> <span class="token operator">//</span> <span class="token number">2</span>


<span class="token keyword">class</span> <span class="token class-name">LeafNode</span><span class="token punctuation">(</span><span class="token builtin">object</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token triple-quoted-string string">"""
    Class : B+ Tree Leaf Node
    represents leaf node in B+ tree
    """</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> degree<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        self<span class="token punctuation">.</span>degree <span class="token operator">=</span> degree
        self<span class="token punctuation">.</span>keys <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>  <span class="token comment"># data values</span>
        self<span class="token punctuation">.</span>sibling <span class="token operator">=</span> <span class="token boolean">None</span>  <span class="token comment"># sibling node to point</span>
        self<span class="token punctuation">.</span>parent <span class="token operator">=</span> <span class="token boolean">None</span>  <span class="token comment"># parent node - None for root node</span>

    <span class="token keyword">def</span> <span class="token function">__repr__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token string">" | "</span><span class="token punctuation">.</span>join<span class="token punctuation">(</span><span class="token builtin">map</span><span class="token punctuation">(</span><span class="token builtin">str</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span>keys<span class="token punctuation">)</span><span class="token punctuation">)</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_leaf</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token boolean">True</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">total_keys</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token builtin">len</span><span class="token punctuation">(</span>self<span class="token punctuation">.</span>keys<span class="token punctuation">)</span>

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_balanced</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token comment"># return False if total keys exceeds max accommodated data (degree - 1)</span>
        <span class="token keyword">return</span> self<span class="token punctuation">.</span>total_keys <span class="token operator">&lt;</span> self<span class="token punctuation">.</span>degree

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_full</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> <span class="token operator">not</span> self<span class="token punctuation">.</span>is_balanced

    @<span class="token builtin">property</span>
    <span class="token keyword">def</span> <span class="token function">is_empty</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">return</span> self<span class="token punctuation">.</span>total_keys <span class="token operator">&lt;</span> math<span class="token punctuation">.</span>floor<span class="token punctuation">(</span>self<span class="token punctuation">.</span>degree <span class="token operator">/</span> <span class="token number">2</span><span class="token punctuation">)</span>


<span class="token keyword">class</span> <span class="token class-name">BPlusTree</span><span class="token punctuation">(</span><span class="token builtin">object</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">def</span> <span class="token function">__init__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> degree<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        self<span class="token punctuation">.</span>degree <span class="token operator">=</span> degree
        self<span class="token punctuation">.</span>__root <span class="token operator">=</span> LeafNode<span class="token punctuation">(</span>degree<span class="token operator">=</span>degree<span class="token punctuation">)</span>
        self<span class="token punctuation">.</span>__leaf <span class="token operator">=</span> self<span class="token punctuation">.</span>__root

    <span class="token keyword">def</span> <span class="token function">search_key</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> start_node<span class="token punctuation">,</span> value<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""

        :param start_node: get root or any non leaf node
        :param value: value to be search
        :return: most matching leaf node
        """</span>
        <span class="token keyword">if</span> start_node<span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>
            _index <span class="token operator">=</span> bisect_left<span class="token punctuation">(</span>start_node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> value<span class="token punctuation">)</span>
            <span class="token keyword">return</span> _index<span class="token punctuation">,</span> start_node
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            _index <span class="token operator">=</span> bisect_right<span class="token punctuation">(</span>start_node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> value<span class="token punctuation">)</span>
            <span class="token keyword">return</span> self<span class="token punctuation">.</span>search_key<span class="token punctuation">(</span>start_node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">,</span> value<span class="token punctuation">)</span>

    <span class="token keyword">def</span> <span class="token function">search</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> start<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">,</span> end<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token triple-quoted-string string">"""

        :param start: specify start node to search range for
        :param end: specify end node for range search
        :return:
        """</span>
        _result <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
        node <span class="token operator">=</span> self<span class="token punctuation">.</span>__root
        leaf <span class="token operator">=</span> self<span class="token punctuation">.</span>__leaf

        <span class="token keyword">if</span> start <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>
            <span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>
                <span class="token keyword">for</span> value <span class="token keyword">in</span> leaf<span class="token punctuation">.</span>keys<span class="token punctuation">:</span>
                    <span class="token keyword">if</span> value <span class="token operator">&lt;=</span> end<span class="token punctuation">:</span>
                        _result<span class="token punctuation">.</span>append<span class="token punctuation">(</span>value<span class="token punctuation">)</span>
                    <span class="token keyword">else</span><span class="token punctuation">:</span>
                        <span class="token keyword">return</span> _result
                <span class="token keyword">if</span> leaf<span class="token punctuation">.</span>sibling <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>
                    <span class="token keyword">return</span> _result
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    leaf <span class="token operator">=</span> leaf<span class="token punctuation">.</span>sibling
        <span class="token keyword">elif</span> end <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>
            _index<span class="token punctuation">,</span> leaf <span class="token operator">=</span> self<span class="token punctuation">.</span>search_key<span class="token punctuation">(</span>node<span class="token punctuation">,</span> start<span class="token punctuation">)</span>
            _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>leaf<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>_index<span class="token punctuation">:</span><span class="token punctuation">]</span><span class="token punctuation">)</span>  <span class="token comment"># equivalent to _result + leaf</span>
            <span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>
                <span class="token keyword">if</span> leaf<span class="token punctuation">.</span>sibling <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>
                    <span class="token keyword">return</span> _result
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    leaf <span class="token operator">=</span> leaf<span class="token punctuation">.</span>sibling
                    _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>leaf<span class="token punctuation">.</span>keys<span class="token punctuation">)</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            <span class="token keyword">if</span> start <span class="token operator">==</span> end<span class="token punctuation">:</span>
                _index<span class="token punctuation">,</span> _node <span class="token operator">=</span> self<span class="token punctuation">.</span>search_key<span class="token punctuation">(</span>node<span class="token punctuation">,</span> start<span class="token punctuation">)</span>
                <span class="token keyword">try</span><span class="token punctuation">:</span>
                    <span class="token keyword">if</span> _node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>_index<span class="token punctuation">]</span> <span class="token operator">==</span> start<span class="token punctuation">:</span>
                        _result<span class="token punctuation">.</span>append<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">)</span>
                        <span class="token keyword">return</span> _result
                    <span class="token keyword">else</span><span class="token punctuation">:</span>
                        <span class="token keyword">return</span> _result
                <span class="token keyword">except</span> IndexError<span class="token punctuation">:</span>
                    <span class="token keyword">return</span> _result
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                _index1<span class="token punctuation">,</span> _node1 <span class="token operator">=</span> self<span class="token punctuation">.</span>search_key<span class="token punctuation">(</span>node<span class="token punctuation">,</span> start<span class="token punctuation">)</span>
                _index2<span class="token punctuation">,</span> _node2 <span class="token operator">=</span> self<span class="token punctuation">.</span>search_key<span class="token punctuation">(</span>node<span class="token punctuation">,</span> end<span class="token punctuation">)</span>
                <span class="token keyword">if</span> _node1 <span class="token keyword">is</span> _node2<span class="token punctuation">:</span>
                    <span class="token keyword">if</span> _index1 <span class="token operator">==</span> _index2<span class="token punctuation">:</span>
                        <span class="token keyword">return</span> _result
                    <span class="token keyword">else</span><span class="token punctuation">:</span>
                        _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>_node1<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>_index1<span class="token punctuation">:</span>_index2<span class="token punctuation">]</span><span class="token punctuation">)</span>
                        <span class="token keyword">return</span> _result
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>_node1<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>_index1<span class="token punctuation">:</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
                    node_ <span class="token operator">=</span> _node1
                    <span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>
                        <span class="token keyword">if</span> _node1<span class="token punctuation">.</span>sibling <span class="token operator">==</span> _node2<span class="token punctuation">:</span>
                            _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>_node2<span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token punctuation">:</span>_index2 <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
                            <span class="token keyword">return</span> _result
                        <span class="token keyword">else</span><span class="token punctuation">:</span>
                            <span class="token keyword">try</span><span class="token punctuation">:</span>
                                _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>node_<span class="token punctuation">.</span>sibling<span class="token punctuation">.</span>keys<span class="token punctuation">)</span>
                                node_ <span class="token operator">=</span> node_<span class="token punctuation">.</span>sibling
                            <span class="token keyword">except</span> AttributeError<span class="token punctuation">:</span>
                                <span class="token keyword">return</span> _result

    <span class="token keyword">def</span> <span class="token function">traverse</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> _node<span class="token punctuation">)</span><span class="token punctuation">:</span>
        _result <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
        _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>keys<span class="token punctuation">)</span>
        <span class="token keyword">if</span> <span class="token builtin">getattr</span><span class="token punctuation">(</span>_node<span class="token punctuation">,</span> <span class="token string">"sibling"</span><span class="token punctuation">,</span> <span class="token boolean">None</span><span class="token punctuation">)</span> <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>
            <span class="token keyword">return</span> _result
        <span class="token keyword">for</span> i <span class="token keyword">in</span> <span class="token builtin">range</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token builtin">len</span><span class="token punctuation">(</span>_node<span class="token punctuation">.</span>sibling<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">[</span><span class="token punctuation">:</span><span class="token punctuation">:</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
            _result<span class="token punctuation">.</span>extend<span class="token punctuation">(</span>self<span class="token punctuation">.</span>traverse<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>sibling<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        <span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>
            <span class="token keyword">pass</span>

    <span class="token keyword">def</span> <span class="token function">pretty_print</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token comment"># print("B+ Tree:")</span>
        queue<span class="token punctuation">,</span> height <span class="token operator">=</span> deque<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token number">0</span>
        queue<span class="token punctuation">.</span>append<span class="token punctuation">(</span><span class="token punctuation">[</span>self<span class="token punctuation">.</span>__root<span class="token punctuation">,</span> height<span class="token punctuation">]</span><span class="token punctuation">)</span>
        <span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>
            <span class="token keyword">try</span><span class="token punctuation">:</span>
                node<span class="token punctuation">,</span> height_ <span class="token operator">=</span> queue<span class="token punctuation">.</span>popleft<span class="token punctuation">(</span><span class="token punctuation">)</span>
                <span class="token comment"># print("adding node: {}".format(node))</span>
            <span class="token keyword">except</span> IndexError<span class="token punctuation">:</span>
                <span class="token keyword">return</span>
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                <span class="token keyword">if</span> <span class="token operator">not</span> node<span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>
                    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Internal Node : {:} \theight &gt;&gt; {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> height_<span class="token punctuation">)</span><span class="token punctuation">)</span>
                    <span class="token keyword">if</span> height_ <span class="token operator">==</span> height<span class="token punctuation">:</span>
                        height <span class="token operator">+=</span> <span class="token number">1</span>
                    queue<span class="token punctuation">.</span>extend<span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">[</span>i<span class="token punctuation">,</span> height<span class="token punctuation">]</span> <span class="token keyword">for</span> i <span class="token keyword">in</span> node<span class="token punctuation">.</span>children<span class="token punctuation">]</span><span class="token punctuation">)</span>
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Leaf Node     : {} \theight &gt;&gt; {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span><span class="token punctuation">[</span>i <span class="token keyword">for</span> i <span class="token keyword">in</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">]</span><span class="token punctuation">,</span> height_<span class="token punctuation">)</span><span class="token punctuation">)</span>

    <span class="token keyword">def</span> <span class="token function">insert</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> value<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token comment"># log("parent:{} leaf:{} node:{}\tkeys:{}\t children:{}".format(node.parent, node.is_leaf, node, node.keys, getattr(node, 'children', '0')))</span>

        <span class="token keyword">def</span> <span class="token function">split_leaf_node</span><span class="token punctuation">(</span>node<span class="token punctuation">)</span><span class="token punctuation">:</span>
            log<span class="token punctuation">(</span><span class="token string">"splitting leaf node: {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">)</span><span class="token punctuation">)</span>
            mid <span class="token operator">=</span> self<span class="token punctuation">.</span>degree <span class="token operator">//</span> <span class="token number">2</span>  <span class="token comment"># integer division in python3</span>
            new_leaf <span class="token operator">=</span> LeafNode<span class="token punctuation">(</span>self<span class="token punctuation">.</span>degree<span class="token punctuation">)</span>
            new_leaf<span class="token punctuation">.</span>keys <span class="token operator">=</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>mid<span class="token punctuation">:</span><span class="token punctuation">]</span>
            <span class="token keyword">if</span> node<span class="token punctuation">.</span>parent <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>  <span class="token comment"># None and 0 are to be treated as different value</span>
                parent_node <span class="token operator">=</span> InternalNode<span class="token punctuation">(</span>self<span class="token punctuation">.</span>degree<span class="token punctuation">)</span>  <span class="token comment"># create new parent for node</span>
                parent_node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> parent_node<span class="token punctuation">.</span>children <span class="token operator">=</span> <span class="token punctuation">[</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>mid<span class="token punctuation">]</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token punctuation">[</span>node<span class="token punctuation">,</span> new_leaf<span class="token punctuation">]</span>
                node<span class="token punctuation">.</span>parent <span class="token operator">=</span> new_leaf<span class="token punctuation">.</span>parent <span class="token operator">=</span> parent_node
                self<span class="token punctuation">.</span>__root <span class="token operator">=</span> parent_node
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                _index <span class="token operator">=</span> node<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>children<span class="token punctuation">.</span>index<span class="token punctuation">(</span>node<span class="token punctuation">)</span>
                node<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>keys<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>_index<span class="token punctuation">,</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>mid<span class="token punctuation">]</span><span class="token punctuation">)</span>
                node<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>children<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>_index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">,</span> new_leaf<span class="token punctuation">)</span>
                new_leaf<span class="token punctuation">.</span>parent <span class="token operator">=</span> node<span class="token punctuation">.</span>parent
                <span class="token keyword">if</span> <span class="token operator">not</span> node<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>is_balanced<span class="token punctuation">:</span>
                    split_internal_node<span class="token punctuation">(</span>node<span class="token punctuation">.</span>parent<span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>keys <span class="token operator">=</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token punctuation">:</span>mid<span class="token punctuation">]</span>
            node<span class="token punctuation">.</span>sibling <span class="token operator">=</span> new_leaf
            log<span class="token punctuation">(</span><span class="token string">"{} --- {} --- {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>node<span class="token punctuation">,</span> node<span class="token punctuation">.</span>sibling<span class="token punctuation">,</span> self<span class="token punctuation">.</span>__root<span class="token punctuation">.</span>children<span class="token punctuation">)</span><span class="token punctuation">)</span>

        <span class="token keyword">def</span> <span class="token function">split_internal_node</span><span class="token punctuation">(</span>node_<span class="token punctuation">)</span><span class="token punctuation">:</span>
            mid <span class="token operator">=</span> self<span class="token punctuation">.</span>degree <span class="token operator">//</span> <span class="token number">2</span>  <span class="token comment"># integer division in python3</span>
            new_node <span class="token operator">=</span> InternalNode<span class="token punctuation">(</span>self<span class="token punctuation">.</span>degree<span class="token punctuation">)</span>
            new_node<span class="token punctuation">.</span>keys <span class="token operator">=</span> node_<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>mid<span class="token punctuation">:</span><span class="token punctuation">]</span>
            new_node<span class="token punctuation">.</span>children <span class="token operator">=</span> node_<span class="token punctuation">.</span>children<span class="token punctuation">[</span>mid<span class="token punctuation">:</span><span class="token punctuation">]</span>
            new_node<span class="token punctuation">.</span>parent <span class="token operator">=</span> node_<span class="token punctuation">.</span>parent
            <span class="token keyword">for</span> child <span class="token keyword">in</span> new_node<span class="token punctuation">.</span>children<span class="token punctuation">:</span>
                child<span class="token punctuation">.</span>parent <span class="token operator">=</span> new_node  <span class="token comment"># assign parent to every new child of current node</span>
            <span class="token keyword">if</span> node_<span class="token punctuation">.</span>parent <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span>  <span class="token comment"># again Note that None and 0 are not same but both treated as False in boolean</span>
                <span class="token comment"># need to make new root if we are to split root node</span>
                new_root <span class="token operator">=</span> InternalNode<span class="token punctuation">(</span>self<span class="token punctuation">.</span>degree<span class="token punctuation">)</span>
                new_root<span class="token punctuation">.</span>keys <span class="token operator">=</span> <span class="token punctuation">[</span>node_<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>mid <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">]</span>
                new_root<span class="token punctuation">.</span>children <span class="token operator">=</span> <span class="token punctuation">[</span>node_<span class="token punctuation">,</span> new_node<span class="token punctuation">]</span>
                node_<span class="token punctuation">.</span>parent <span class="token operator">=</span> new_node<span class="token punctuation">.</span>parent <span class="token operator">=</span> new_root  <span class="token comment"># set parent of newly created node</span>
                self<span class="token punctuation">.</span>__root <span class="token operator">=</span> new_root  <span class="token comment"># set new ROOT node</span>
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                <span class="token comment"># if node is not root internal node</span>
                _index <span class="token operator">=</span> node_<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>children<span class="token punctuation">.</span>index<span class="token punctuation">(</span>node_<span class="token punctuation">)</span>
                node_<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>keys<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>_index<span class="token punctuation">,</span> node_<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>mid <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
                node_<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>children<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>_index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">,</span> new_node<span class="token punctuation">)</span>
                <span class="token keyword">if</span> <span class="token operator">not</span> node_<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>is_balanced<span class="token punctuation">:</span>
                    split_internal_node<span class="token punctuation">(</span>node_<span class="token punctuation">.</span>parent<span class="token punctuation">)</span>
            node_<span class="token punctuation">.</span>keys <span class="token operator">=</span> node_<span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token punctuation">:</span>mid <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">]</span>
            node_<span class="token punctuation">.</span>children <span class="token operator">=</span> node_<span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token punctuation">:</span>mid<span class="token punctuation">]</span>
            <span class="token keyword">return</span> node_<span class="token punctuation">.</span>parent

        <span class="token keyword">def</span> <span class="token function">insert_node</span><span class="token punctuation">(</span>_node<span class="token punctuation">)</span><span class="token punctuation">:</span>
            log<span class="token punctuation">(</span><span class="token string">"inserting : {} in node: {} having children: {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>value<span class="token punctuation">,</span> _node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> <span class="token builtin">getattr</span><span class="token punctuation">(</span>_node<span class="token punctuation">,</span> <span class="token string">"children"</span><span class="token punctuation">,</span> <span class="token string">"NULL"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            <span class="token keyword">if</span> _node<span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>  <span class="token comment"># logic for leaf node</span>
                log<span class="token punctuation">(</span><span class="token string">"node: {} is leaf"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>_node<span class="token punctuation">)</span><span class="token punctuation">)</span>
                _index <span class="token operator">=</span> bisect_right<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> value<span class="token punctuation">)</span>  <span class="token comment"># bisect and get index value of where to insert value in node.keys</span>
                _node<span class="token punctuation">.</span>keys<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>_index<span class="token punctuation">,</span> value<span class="token punctuation">)</span>
                <span class="token keyword">if</span> <span class="token operator">not</span> _node<span class="token punctuation">.</span>is_balanced<span class="token punctuation">:</span>
                    split_leaf_node<span class="token punctuation">(</span>_node<span class="token punctuation">)</span>
                    log<span class="token punctuation">(</span><span class="token string">"----------- Tree status after split---------------"</span><span class="token punctuation">)</span>
                    log<span class="token punctuation">(</span>self<span class="token punctuation">.</span>__root<span class="token punctuation">)</span>
                    log<span class="token punctuation">(</span>self<span class="token punctuation">.</span>__root<span class="token punctuation">.</span>children<span class="token punctuation">)</span>
                    log<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>parent<span class="token punctuation">.</span>children<span class="token punctuation">)</span>
                    log<span class="token punctuation">(</span><span class="token builtin">getattr</span><span class="token punctuation">(</span>self<span class="token punctuation">.</span>__root<span class="token punctuation">,</span> <span class="token string">"children"</span><span class="token punctuation">,</span> <span class="token string">"NULL"</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    <span class="token keyword">return</span>
            <span class="token keyword">else</span><span class="token punctuation">:</span>  <span class="token comment"># logic for internal node</span>
                <span class="token keyword">if</span> <span class="token operator">not</span> _node<span class="token punctuation">.</span>is_balanced<span class="token punctuation">:</span>
                    self<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>split_internal_node<span class="token punctuation">(</span>_node<span class="token punctuation">)</span><span class="token punctuation">)</span>
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    _index <span class="token operator">=</span> bisect_right<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> value<span class="token punctuation">)</span>
                    log<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> _node<span class="token punctuation">.</span>children<span class="token punctuation">,</span> _index<span class="token punctuation">)</span>
                    insert_node<span class="token punctuation">(</span>_node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">)</span>

        insert_node<span class="token punctuation">(</span>self<span class="token punctuation">.</span>__root<span class="token punctuation">)</span>

    @<span class="token builtin">staticmethod</span>
    <span class="token keyword">def</span> <span class="token function">traverse_left_to_right</span><span class="token punctuation">(</span>node<span class="token punctuation">,</span> index<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">if</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>insert<span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>pop<span class="token punctuation">(</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>index<span class="token punctuation">]</span> <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">.</span>insert<span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token operator">-</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>parent <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>insert<span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">.</span>pop<span class="token punctuation">(</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>pop<span class="token punctuation">(</span><span class="token punctuation">)</span>

    @<span class="token builtin">staticmethod</span>
    <span class="token keyword">def</span> <span class="token function">traverse_right_to_left</span><span class="token punctuation">(</span>node<span class="token punctuation">,</span> index<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">if</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>append<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>remove<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>index<span class="token punctuation">]</span> <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">.</span>append<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>parent <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>append<span class="token punctuation">(</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>index<span class="token punctuation">]</span> <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">.</span>remove<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">.</span>remove<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span>

    <span class="token keyword">def</span> <span class="token function">delete</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> delete_value<span class="token punctuation">)</span><span class="token punctuation">:</span>
        <span class="token keyword">def</span> <span class="token function">merge</span><span class="token punctuation">(</span>node<span class="token punctuation">,</span> index<span class="token punctuation">)</span><span class="token punctuation">:</span>
            <span class="token keyword">if</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>
                node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys <span class="token operator">+</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys
                node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>sibling <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>sibling
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>keys <span class="token operator">+</span> <span class="token punctuation">[</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">]</span> <span class="token operator">+</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>
                    index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>keys
                node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>children <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">.</span>children <span class="token operator">+</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>children
            node<span class="token punctuation">.</span>children<span class="token punctuation">.</span>remove<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
            node<span class="token punctuation">.</span>keys<span class="token punctuation">.</span>remove<span class="token punctuation">(</span>node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>index<span class="token punctuation">]</span><span class="token punctuation">)</span>
            <span class="token keyword">if</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">:</span>
                <span class="token keyword">return</span> node
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                node<span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>parent <span class="token operator">=</span> <span class="token boolean">None</span>
                self<span class="token punctuation">.</span>__root <span class="token operator">=</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
                <span class="token keyword">del</span> node
                <span class="token keyword">return</span> self<span class="token punctuation">.</span>__root

        <span class="token keyword">def</span> <span class="token function">delete_node</span><span class="token punctuation">(</span>value<span class="token punctuation">,</span> node<span class="token punctuation">)</span><span class="token punctuation">:</span>
            log<span class="token punctuation">(</span><span class="token string">"deleting {} from node: {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>value<span class="token punctuation">,</span> node<span class="token punctuation">)</span><span class="token punctuation">)</span>
            <span class="token keyword">if</span> node<span class="token punctuation">.</span>is_leaf<span class="token punctuation">:</span>
                log<span class="token punctuation">(</span><span class="token string">"node is leaf"</span><span class="token punctuation">)</span>
                _index <span class="token operator">=</span> bisect_left<span class="token punctuation">(</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> value<span class="token punctuation">)</span>
                <span class="token keyword">try</span><span class="token punctuation">:</span>
                    node_ <span class="token operator">=</span> node<span class="token punctuation">.</span>keys<span class="token punctuation">[</span>_index<span class="token punctuation">]</span>
                <span class="token keyword">except</span> IndexError<span class="token punctuation">:</span>
                    <span class="token keyword">return</span> <span class="token boolean">False</span>
                <span class="token keyword">else</span><span class="token punctuation">:</span>
                    <span class="token keyword">if</span> node_ <span class="token operator">!=</span> value<span class="token punctuation">:</span>
                        <span class="token keyword">return</span> <span class="token boolean">False</span>
                    <span class="token keyword">else</span><span class="token punctuation">:</span>
                        node<span class="token punctuation">.</span>keys<span class="token punctuation">.</span>remove<span class="token punctuation">(</span>value<span class="token punctuation">)</span>
                        <span class="token keyword">return</span> <span class="token boolean">True</span>
            <span class="token keyword">else</span><span class="token punctuation">:</span>
                log<span class="token punctuation">(</span><span class="token string">"traversing internal node for deleting value"</span><span class="token punctuation">)</span>
                _index <span class="token operator">=</span> bisect_right<span class="token punctuation">(</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">,</span> value<span class="token punctuation">)</span>
                log<span class="token punctuation">(</span><span class="token string">"encountered index: {} having child values: {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>_index<span class="token punctuation">,</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
                <span class="token keyword">if</span> _index <span class="token operator">&lt;=</span> <span class="token builtin">len</span><span class="token punctuation">(</span>node<span class="token punctuation">.</span>keys<span class="token punctuation">)</span><span class="token punctuation">:</span>
                    <span class="token comment"># print(node.children[_index].is_leaf)</span>
                    <span class="token comment"># print(node.children[_index], node.children[_index].total_keys, node.children[_index].degree / 2, node.children[_index].is_empty)</span>
                    <span class="token keyword">if</span> <span class="token operator">not</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">.</span>is_empty<span class="token punctuation">:</span>
                        <span class="token keyword">return</span> delete_node<span class="token punctuation">(</span>value<span class="token punctuation">,</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">)</span>
                    <span class="token keyword">elif</span> <span class="token operator">not</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span>is_empty<span class="token punctuation">:</span>
                        self<span class="token punctuation">.</span>traverse_left_to_right<span class="token punctuation">(</span>node<span class="token punctuation">,</span> _index <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">)</span>
                        <span class="token keyword">return</span> delete_node<span class="token punctuation">(</span>value<span class="token punctuation">,</span> node<span class="token punctuation">.</span>children<span class="token punctuation">[</span>_index<span class="token punctuation">]</span><span class="token punctuation">)</span>
                    <span class="token keyword">else</span><span class="token punctuation">:</span>
                        <span class="token keyword">return</span> delete_node<span class="token punctuation">(</span>value<span class="token punctuation">,</span> merge<span class="token punctuation">(</span>node<span class="token punctuation">,</span> _index<span class="token punctuation">)</span><span class="token punctuation">)</span>
        delete_node<span class="token punctuation">(</span>delete_value<span class="token punctuation">,</span> self<span class="token punctuation">.</span>__root<span class="token punctuation">)</span>

<span class="token keyword">def</span> <span class="token function">_test</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token comment"># test_lis = [0, 1, 11, 1, 2, 22, 13, 14, 4, 5, 23, 1, 51, 12, 31]</span>
    test_lis <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">159</span><span class="token punctuation">,</span> <span class="token number">200</span><span class="token punctuation">,</span> <span class="token number">18</span><span class="token punctuation">,</span> <span class="token number">90</span><span class="token punctuation">,</span> <span class="token number">8</span><span class="token punctuation">,</span> <span class="token number">17</span><span class="token punctuation">,</span> <span class="token number">9</span><span class="token punctuation">]</span>
    <span class="token comment"># test_lis = range(10)</span>
    b <span class="token operator">=</span> BPlusTree<span class="token punctuation">(</span>degree<span class="token operator">=</span><span class="token number">4</span><span class="token punctuation">)</span>
    <span class="token keyword">for</span> val <span class="token keyword">in</span> test_lis<span class="token punctuation">:</span>
        b<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>val<span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"----------- B+ TREE AFTER INSERT : {:3d} -----------"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>val<span class="token punctuation">)</span><span class="token punctuation">)</span>
        b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token comment"># print("searching range..........")</span>
    <span class="token comment"># result = b.search_range(1, 12)</span>
    search_start<span class="token punctuation">,</span> search_end <span class="token operator">=</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">23</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"----- Searching in batch for {} to {} -----"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>search_start<span class="token punctuation">,</span> search_end<span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Result*: {} \n (*distinct values)"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>b<span class="token punctuation">.</span>search<span class="token punctuation">(</span>search_start<span class="token punctuation">,</span> search_end<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">for</span> delete_val <span class="token keyword">in</span> <span class="token punctuation">[</span><span class="token number">200</span><span class="token punctuation">,</span> <span class="token number">18</span><span class="token punctuation">,</span> <span class="token number">9</span><span class="token punctuation">]</span><span class="token punctuation">:</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"----- DELETING {} -----"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>delete_val<span class="token punctuation">)</span><span class="token punctuation">)</span>
        b<span class="token punctuation">.</span>delete<span class="token punctuation">(</span>delete_val<span class="token punctuation">)</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"----------- B+ TREE AFTER DELETING : {:3d} -----------"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>delete_val<span class="token punctuation">)</span><span class="token punctuation">)</span>
        b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>


<span class="token keyword">if</span> __name__ <span class="token operator">==</span> <span class="token string">"__main__"</span><span class="token punctuation">:</span>
    <span class="token keyword">from</span> collections <span class="token keyword">import</span> OrderedDict
    choices <span class="token operator">=</span> OrderedDict<span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token number">1</span><span class="token punctuation">:</span> <span class="token string">"Insert"</span><span class="token punctuation">,</span>
        <span class="token number">2</span><span class="token punctuation">:</span> <span class="token string">"Batch Insert"</span><span class="token punctuation">,</span>
        <span class="token number">3</span><span class="token punctuation">:</span> <span class="token string">"Delete"</span><span class="token punctuation">,</span>
        <span class="token number">4</span><span class="token punctuation">:</span> <span class="token string">"Search"</span><span class="token punctuation">,</span>
        <span class="token number">5</span><span class="token punctuation">:</span> <span class="token string">"Search Range"</span><span class="token punctuation">,</span>
        <span class="token number">6</span><span class="token punctuation">:</span> <span class="token string">"Terminate"</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    degree <span class="token operator">=</span> <span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter Degree of tree[4]: "</span><span class="token punctuation">)</span>
    b <span class="token operator">=</span> BPlusTree<span class="token punctuation">(</span>degree<span class="token operator">=</span><span class="token builtin">int</span><span class="token punctuation">(</span>degree<span class="token punctuation">)</span> <span class="token keyword">if</span> degree <span class="token keyword">else</span> <span class="token number">4</span><span class="token punctuation">)</span>
    <span class="token keyword">while</span> <span class="token boolean">True</span><span class="token punctuation">:</span>
        <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"\n"</span><span class="token punctuation">.</span>join<span class="token punctuation">(</span><span class="token string">"{} {}"</span><span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>key<span class="token punctuation">,</span> val<span class="token punctuation">)</span> <span class="token keyword">for</span> key<span class="token punctuation">,</span> val <span class="token keyword">in</span> choices<span class="token punctuation">.</span>items<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        choice <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter Choice: "</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        <span class="token keyword">if</span> choice <span class="token operator">==</span> <span class="token number">1</span><span class="token punctuation">:</span>
            val <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter number to insert: "</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>val<span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">elif</span> choice <span class="token operator">==</span> <span class="token number">2</span><span class="token punctuation">:</span>
            _values <span class="token operator">=</span> <span class="token builtin">map</span><span class="token punctuation">(</span><span class="token builtin">int</span><span class="token punctuation">,</span> <span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter numbers (space separated): "</span><span class="token punctuation">)</span><span class="token punctuation">.</span>split<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            <span class="token keyword">for</span> val <span class="token keyword">in</span> _values<span class="token punctuation">:</span>
                b<span class="token punctuation">.</span>insert<span class="token punctuation">(</span>val<span class="token punctuation">)</span>
                b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">elif</span> choice <span class="token operator">==</span> <span class="token number">3</span><span class="token punctuation">:</span>
            val <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter number to delete: "</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>delete<span class="token punctuation">(</span>val<span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">elif</span> choice <span class="token operator">==</span> <span class="token number">4</span><span class="token punctuation">:</span>
            val <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter number to search: "</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>search<span class="token punctuation">(</span>val<span class="token punctuation">,</span> val<span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">elif</span> choice <span class="token operator">==</span> <span class="token number">5</span><span class="token punctuation">:</span>
            start <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter start number of range: "</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            end <span class="token operator">=</span> <span class="token builtin">int</span><span class="token punctuation">(</span><span class="token builtin">input</span><span class="token punctuation">(</span><span class="token string">"Enter end number of range: "</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>search<span class="token punctuation">(</span>start<span class="token punctuation">,</span> end<span class="token punctuation">)</span>
            b<span class="token punctuation">.</span>pretty_print<span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token keyword">else</span><span class="token punctuation">:</span>
            <span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"Thanks for using the service!!"</span><span class="token punctuation">)</span>
            <span class="token keyword">break</span>
</code></pre>
<h2 id="analysis">Analysis</h2>
<ul>
<li>all leaves at the same lowest level</li>
<li>all nodes at least half full (except root)<br>
Let 𝑓 be the degree of tree and n be the total number of data then</li>
</ul>

<table>
<thead>
<tr>
<th align="right"></th>
<th align="center">Max # pointers</th>
<th align="center">Max # keys</th>
<th align="center">Min # pointers</th>
<th align="center">Min # keys</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">Non-leaf</td>
<td align="center">𝑓</td>
<td align="center">𝑓 − 1</td>
<td align="center">⌈𝑓/2⌉</td>
<td align="center">⌈𝑓/2⌉ − 1</td>
</tr>
<tr>
<td align="right">Root</td>
<td align="center">𝑓</td>
<td align="center">𝑓 − 1</td>
<td align="center">2</td>
<td align="center">1</td>
</tr>
<tr>
<td align="right">Leaf</td>
<td align="center">𝑓</td>
<td align="center">𝑓 − 1</td>
<td align="center">⌊𝑓/2⌋</td>
<td align="center">⌊𝑓/2⌋</td>
</tr>
</tbody>
</table><ul>
<li>Number of disk accesses proportional to the height of the B-tree.</li>
<li>The <em><strong>worst-case height</strong></em> of a B+ tree is:<br>
<span class="katex--display"><span class="katex-display"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>h</mi><mo>∝</mo><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mfrac><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow><mn>2</mn></mfrac><mo>∼</mo><mi>O</mi><mo>(</mo><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">  
h \propto \log_f{\frac{n +1}{2}} \sim O(\log_fn)
</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.69444em; vertical-align: 0em;"></span><span class="mord mathit">h</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">∝</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 2.00744em; vertical-align: -0.686em;"></span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord"><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 1.32144em;"><span class="" style="top: -2.314em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord">2</span></span></span><span class="" style="top: -3.23em;"><span class="pstrut" style="height: 3em;"></span><span class="frac-line" style="border-bottom-width: 0.04em;"></span></span><span class="" style="top: -3.677em;"><span class="pstrut" style="height: 3em;"></span><span class="mord"><span class="mord mathit">n</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right: 0.222222em;"></span><span class="mord">1</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.686em;"><span class=""></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">∼</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></span></li>
</ul>

<table>
<thead>
<tr>
<th align="right"></th>
<th>Time Complexity</th>
<th>Remarks</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">height</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td></td>
</tr>
<tr>
<td align="right">search</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><mi>f</mi><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(f\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span style="margin-right: 0.10764em;" class="mord mathit">f</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td>linear search inside each nodes</td>
</tr>
<tr>
<td align="right">search</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><msub><mi>log</mi><mo>⁡</mo><mn>2</mn></msub><mi>f</mi><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(\log_2f\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.206968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.24414em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span style="margin-right: 0.10764em;" class="mord mathit">f</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td>binary search inside each node</td>
</tr>
<tr>
<td align="right">insert</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td>if splitting not require</td>
</tr>
<tr>
<td align="right">insert</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><mi>f</mi><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(f\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span style="margin-right: 0.10764em;" class="mord mathit">f</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td>if splitting require</td>
</tr>
<tr>
<td align="right">insert</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td>if merge not require</td>
</tr>
<tr>
<td align="right">insert</td>
<td><span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>O</mi><mo>(</mo><mi>f</mi><msub><mi>log</mi><mo>⁡</mo><mi>f</mi></msub><mi>n</mi><mo>)</mo></mrow><annotation encoding="application/x-tex">O(f\log_fn)</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1.13025em; vertical-align: -0.380248em;"></span><span style="margin-right: 0.02778em;" class="mord mathit">O</span><span class="mopen">(</span><span style="margin-right: 0.10764em;" class="mord mathit">f</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mop"><span class="mop">lo<span style="margin-right: 0.01389em;">g</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.241968em;"><span class="" style="top: -2.45586em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span style="margin-right: 0.10764em;" class="mord mathit mtight">f</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.380248em;"><span class=""></span></span></span></span></span></span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord mathit">n</span><span class="mclose">)</span></span></span></span></span></td>
<td>if merge require</td>
</tr>
</tbody>
</table>
