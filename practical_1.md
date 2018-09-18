---


---

<h1 id="practical-1">Practical 1</h1>
<blockquote>
<p>a) Import Database, understand Query execution plan using SQL Yog<br>
b) Analyze impact of index , type of index on query performance</p>
</blockquote>
<h2 id="a-database-structure">a) Database Structure</h2>
<ul>
<li><strong>Database</strong>: <em>MySQL</em></li>
<li><strong>Total data rows in table ds_leaderboard</strong>: <em>4,00,000</em></li>
<li>PC Configuration<br>
<em>: Intel® Core™ i3-4130 CPU @ 3.40GHz × 4<br>
: ~ 4 GB RAM</em></li>
</ul>
<p><em>Table</em>: <strong>ds_leaderboard</strong></p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">CREATE</span> <span class="token keyword">TABLE</span> <span class="token punctuation">`</span>ds_leaderboard<span class="token punctuation">`</span> <span class="token punctuation">(</span>     
   <span class="token punctuation">`</span>id<span class="token punctuation">`</span> <span class="token keyword">Int</span><span class="token punctuation">(</span> <span class="token number">11</span> <span class="token punctuation">)</span> <span class="token keyword">AUTO_INCREMENT</span> <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>    
   <span class="token punctuation">`</span>name<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">64</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
   <span class="token punctuation">`</span>email<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">254</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
   <span class="token punctuation">`</span>organizer<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">256</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
   <span class="token punctuation">`</span>score<span class="token punctuation">`</span> <span class="token keyword">Double</span><span class="token punctuation">(</span> <span class="token number">22</span><span class="token punctuation">,</span> <span class="token number">0</span> <span class="token punctuation">)</span> <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
   <span class="token punctuation">`</span>time<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">16</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
   <span class="token punctuation">`</span>country<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">128</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
   <span class="token punctuation">`</span>language_id<span class="token punctuation">`</span> <span class="token keyword">Int</span><span class="token punctuation">(</span> <span class="token number">11</span> <span class="token punctuation">)</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span> <span class="token keyword">PRIMARY</span> <span class="token keyword">KEY</span> <span class="token punctuation">(</span> <span class="token punctuation">`</span>id<span class="token punctuation">`</span> <span class="token punctuation">)</span>   
<span class="token punctuation">)</span>  
<span class="token keyword">CHARACTER SET</span> <span class="token operator">=</span> utf8    
<span class="token keyword">COLLATE</span> <span class="token operator">=</span> utf8_general_ci    
<span class="token keyword">ENGINE</span> <span class="token operator">=</span> <span class="token keyword">InnoDB</span>    
<span class="token keyword">AUTO_INCREMENT</span> <span class="token operator">=</span> <span class="token number">400001</span><span class="token punctuation">;</span>  
</code></pre>
<hr>
<p><em>Table</em>:<strong>ds_programminglanguage</strong></p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">CREATE</span> <span class="token keyword">TABLE</span> <span class="token punctuation">`</span>ds_programminglanguage<span class="token punctuation">`</span> <span class="token punctuation">(</span>  
  <span class="token punctuation">`</span>id<span class="token punctuation">`</span> <span class="token keyword">Int</span><span class="token punctuation">(</span> <span class="token number">11</span> <span class="token punctuation">)</span> <span class="token keyword">AUTO_INCREMENT</span> <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>    
  <span class="token punctuation">`</span>name<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">32</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token operator">NOT</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
  <span class="token punctuation">`</span>version<span class="token punctuation">`</span> <span class="token keyword">VarChar</span><span class="token punctuation">(</span> <span class="token number">16</span> <span class="token punctuation">)</span> <span class="token keyword">CHARACTER SET</span> utf8 <span class="token keyword">COLLATE</span> utf8_general_ci <span class="token boolean">NULL</span><span class="token punctuation">,</span>   
  <span class="token punctuation">`</span><span class="token keyword">release</span><span class="token punctuation">`</span> <span class="token keyword">Date</span> <span class="token boolean">NULL</span><span class="token punctuation">,</span> <span class="token keyword">PRIMARY</span> <span class="token keyword">KEY</span> <span class="token punctuation">(</span> <span class="token punctuation">`</span>id<span class="token punctuation">`</span> <span class="token punctuation">)</span>   
<span class="token punctuation">)</span>   
<span class="token keyword">CHARACTER SET</span> <span class="token operator">=</span> utf8   
<span class="token keyword">COLLATE</span> <span class="token operator">=</span> utf8_general_ci   
<span class="token keyword">ENGINE</span> <span class="token operator">=</span> <span class="token keyword">InnoDB</span>   
<span class="token keyword">AUTO_INCREMENT</span> <span class="token operator">=</span> <span class="token number">13</span><span class="token punctuation">;</span>  
</code></pre>
<hr>
<h2 id="b-impact-of-index">b) Impact of index</h2>
<h3 id="case-1">Case 1</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard<span class="token punctuation">;</span>  
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">1.947 s</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">Index used</td>
<td align="left">No index to be used because we are loading all data of all attribute(column)</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_all.png" alt=""></p>
</blockquote>
<h3 id="case-2.1--with-index">Case 2.1 : with index</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">where</span> language_id<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span>  
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">234 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">33243</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">index on attribute language_id</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_all_language_1.png" alt=""></p>
</blockquote>
<h3 id="case-2.2--without-index--forced-to-not-to-use">Case 2.2 : without index  (forced to not to use)</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">ignore</span> <span class="token keyword">index</span><span class="token punctuation">(</span>pl<span class="token punctuation">)</span> <span class="token keyword">where</span> language_id<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span>
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">291 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">33243</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">(No index) ignoring index on attribute language_id (index referred as <code>pl</code>)</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_all_language_without_pl.png" alt=""></p>
</blockquote>
<h3 id="case-3.1--with-no-index">Case 3.1 : with no index</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> name<span class="token punctuation">,</span>language_id <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">where</span> language_id <span class="token operator">between</span> <span class="token number">1</span> <span class="token operator">and</span> <span class="token number">5</span><span class="token punctuation">;</span>  
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">215 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">166490</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">(No index used) (possible key on language_id)</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_name.lang_where_lang_range_215ms.png" alt=""></p>
</blockquote>
<h3 id="case-3.2--with-index-on-language_id-force-to-use">Case 3.2 : with index on language_id (force to use)</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> name<span class="token punctuation">,</span>language_id <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">use</span> <span class="token keyword">index</span><span class="token punctuation">(</span>pl<span class="token punctuation">)</span> <span class="token keyword">where</span> language_id <span class="token operator">between</span> <span class="token number">1</span> <span class="token operator">and</span> <span class="token number">5</span><span class="token punctuation">;</span>
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">206 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">166490</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">forced to use index on language_id (pl)</td>
</tr>
</tbody>
</table><p><img src="" alt=""></p>
<h3 id="case-4.1--using-index-on-country">Case 4.1 : using index on country</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">where</span> country<span class="token operator">=</span><span class="token string">'India'</span><span class="token punctuation">;</span>    
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">20 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">1597</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">used index on country</td>
</tr>
</tbody>
</table><p><img src="" alt=""></p>
<h3 id="case-4.2--without-index-forced-to-ignore">Case 4.2 : without index (forced to ignore)</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">ignore</span> <span class="token keyword">index</span><span class="token punctuation">(</span>ctry<span class="token punctuation">)</span> <span class="token keyword">where</span> country<span class="token operator">=</span><span class="token string">'India'</span><span class="token punctuation">;</span>    
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">155 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">1597</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">forced to ignore index on country</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="" alt=""></p>
</blockquote>
<h3 id="case-5.1--using-index-on-language_id-and-country">Case 5.1 : using index on language_id and country</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">where</span> country<span class="token operator">=</span><span class="token string">'India'</span> <span class="token operator">and</span> language_id<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span>    
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">11 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">143</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">Using intersect(pl,ctry); index of language_id and country</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/case5_2_index.png" alt=""></p>
</blockquote>
<h3 id="case-5.2--force-to-ignore-index-on-country">Case 5.2 : force to ignore index on country</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">ignore</span> <span class="token keyword">index</span><span class="token punctuation">(</span>ctry<span class="token punctuation">)</span> <span class="token keyword">where</span> country<span class="token operator">=</span><span class="token string">'India'</span> <span class="token operator">and</span> language_id<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span>    
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">42 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">143</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">Using index on language_id</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="" alt=""></p>
</blockquote>
<h3 id="case-5.3--force-to-ignore-index-on-language_id">Case 5.3 : force to ignore index on language_id</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">ignore</span> <span class="token keyword">index</span><span class="token punctuation">(</span>pl<span class="token punctuation">)</span> <span class="token keyword">where</span> country<span class="token operator">=</span><span class="token string">'India'</span> <span class="token operator">and</span> language_id<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span>
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">4 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">143</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">Using index on country</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/case5_index_on_country.png" alt=""></p>
</blockquote>
<h3 id="case-5.4-without-index">Case 5.4 without index</h3>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">select</span> <span class="token operator">*</span> <span class="token keyword">from</span> ds_leaderboard <span class="token keyword">ignore</span> <span class="token keyword">index</span><span class="token punctuation">(</span>pl<span class="token punctuation">,</span>ctry<span class="token punctuation">)</span> <span class="token keyword">where</span> country<span class="token operator">=</span><span class="token string">'India'</span> <span class="token operator">and</span> language_id<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span>
</code></pre>

<table>
<thead>
<tr>
<th align="right">Query time</th>
<th align="left">148 ms</th>
</tr>
</thead>
<tbody>
<tr>
<td align="right">No. of records</td>
<td align="left">143</td>
</tr>
<tr>
<td align="right">Index used</td>
<td align="left">No index used; Forced to ignore index</td>
</tr>
</tbody>
</table><blockquote>
<p><img src="https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/case5_no_index.png" alt=""></p>
</blockquote>
<h2 id="summary">Summary</h2>
<p>In records of <code>4,00,000</code> entries <code>33,243</code> entries having <em>language_id</em> equals to <code>1</code> (<em>As in Case 2</em>) and just <code>1597</code> entries having <em>country</em> equals to <code>India</code> (<em>As in Case 4</em>)and only <code>143</code> entries having both (<em>As in Case 5</em>).</p>
<p>In <code>case 5.1</code> query engine choose to use index of both attribute language_id (pl) and country (ctry) and intersection of it is displayed which took about <code>11 ms</code> whereas when we forced to use only index on <em>country</em> the result took only <code>4 ms</code> but for only using index on <em>language_id</em>  it costs <code>148 ms</code></p>

