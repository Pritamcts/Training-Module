<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="ChatBot_Project_0"></a>Chat-Bot Project</h1>
<p class="has-line-data" data-line-start="2" data-line-end="3">This project is a chat-bot built using Django, Pinecone vector database, OpenAI, and LangChain. The user interface is implemented using Streamlit. The chat-bot leverages a custom knowledge base to provide responses.</p>
<h2 class="code-line" data-line-start=4 data-line-end=5 ><a id="Features_4"></a>Features</h2>
<ul>
<li class="has-line-data" data-line-start="6" data-line-end="7"><strong>Django</strong>: Backend framework to manage the application.</li>
<li class="has-line-data" data-line-start="7" data-line-end="8"><strong>Django REST framework</strong>: For building robust APIs.</li>
<li class="has-line-data" data-line-start="8" data-line-end="9"><strong>Pinecone</strong>: Vector database to manage and search through embeddings.</li>
<li class="has-line-data" data-line-start="9" data-line-end="10"><strong>OpenAI</strong>: For natural language understanding and response generation.</li>
<li class="has-line-data" data-line-start="10" data-line-end="11"><strong>LangChain</strong>: To facilitate the interaction between the language model and the knowledge base.</li>
<li class="has-line-data" data-line-start="11" data-line-end="12"><strong>Streamlit</strong>: For creating an interactive and user-friendly UI.</li>
<li class="has-line-data" data-line-start="12" data-line-end="13"><strong>Flask</strong>: For handling API requests to store and retrieve data.</li>
<li class="has-line-data" data-line-start="13" data-line-end="15"><strong>PostgreSQL</strong>: Database to store responses and feedback.</li>
</ul>
<h2 class="code-line" data-line-start=15 data-line-end=16 ><a id="Prerequisites_15"></a>Prerequisites</h2>
<ul>
<li class="has-line-data" data-line-start="17" data-line-end="18">Python 3.11.5</li>
<li class="has-line-data" data-line-start="18" data-line-end="19">Django REST framework</li>
<li class="has-line-data" data-line-start="19" data-line-end="20">Flask</li>
<li class="has-line-data" data-line-start="20" data-line-end="21">psycopg2</li>
<li class="has-line-data" data-line-start="21" data-line-end="22">Pinecone API Key</li>
<li class="has-line-data" data-line-start="22" data-line-end="23">OpenAI API Key</li>
<li class="has-line-data" data-line-start="23" data-line-end="24">Streamlit</li>
<li class="has-line-data" data-line-start="24" data-line-end="26">PostgreSQL</li>
</ul>
<h2 class="code-line" data-line-start=26 data-line-end=27 ><a id="Installation_26"></a>Installation</h2>
<ol>
<li class="has-line-data" data-line-start="28" data-line-end="34">
<p class="has-line-data" data-line-start="28" data-line-end="29"><strong>Clone the repository:</strong></p>
<pre><code class="has-line-data" data-line-start="30" data-line-end="33" class="language-bash">git <span class="hljs-built_in">clone</span> https://github.com/your-username/chat-bot-project.git
<span class="hljs-built_in">cd</span> chat-bot-project
</code></pre>
</li>
<li class="has-line-data" data-line-start="34" data-line-end="40">
<p class="has-line-data" data-line-start="34" data-line-end="35"><strong>Create a virtual environment:</strong></p>
<pre><code class="has-line-data" data-line-start="36" data-line-end="39" class="language-bash">python -m venv venv
<span class="hljs-built_in">source</span> venv/bin/activate  <span class="hljs-comment"># On Windows, use `venv\Scripts\activate`</span>
</code></pre>
</li>
<li class="has-line-data" data-line-start="40" data-line-end="45">
<p class="has-line-data" data-line-start="40" data-line-end="41"><strong>Install the required packages:</strong></p>
<pre><code class="has-line-data" data-line-start="42" data-line-end="44" class="language-bash">pip install -r requirements.txt
</code></pre>
</li>
<li class="has-line-data" data-line-start="45" data-line-end="65">
<p class="has-line-data" data-line-start="45" data-line-end="47"><strong>Set up configuration file:</strong><br>
Create a <code>config-dev.json</code> file in the root directory and add your API keys and other necessary configurations:</p>
<pre><code class="has-line-data" data-line-start="48" data-line-end="64" class="language-json">{
  "<span class="hljs-attribute">DIRECTORY_TO_SCAN</span>": <span class="hljs-value"><span class="hljs-string">"C:/Users/User/Downloads/Project/Source/"</span></span>,
  "<span class="hljs-attribute">PROCESSED_FILES</span>": <span class="hljs-value"><span class="hljs-string">"C:/Users/User/Downloads/Project/Processed/"</span></span>,
  "<span class="hljs-attribute">ERROR_FILES</span>": <span class="hljs-value"><span class="hljs-string">"C:/Users/User/Downloads/Project/Error/"</span></span>,
  "<span class="hljs-attribute">PINECONE_API_KEY</span>": <span class="hljs-value"><span class="hljs-string">"your_pinecone_api_key"</span></span>,
  "<span class="hljs-attribute">PINECONE_INDEX</span>": <span class="hljs-value"><span class="hljs-string">"langchain-app"</span></span>,
  "<span class="hljs-attribute">OPENAI_API_KEY</span>": <span class="hljs-value"><span class="hljs-string">"your_openai_api_key"</span></span>,
  "<span class="hljs-attribute">PDF_MODEL</span>": <span class="hljs-value"><span class="hljs-string">"OPENAI"</span></span>,
  "<span class="hljs-attribute">TXT_MODEL</span>": <span class="hljs-value"><span class="hljs-string">"OPENAI"</span></span>,
  "<span class="hljs-attribute">OPEN_AI_PDF_EMBEDDING_MODEL</span>": <span class="hljs-value"><span class="hljs-string">"text-embedding-ada-002"</span></span>,
  "<span class="hljs-attribute">OPEN_AI_PDF_EMBEDDING_CTX_LENGTH</span>": <span class="hljs-value"><span class="hljs-number">8191</span></span>,
  "<span class="hljs-attribute">OPEN_AI_PDF_EMBEDDING_ENCODING</span>": <span class="hljs-value"><span class="hljs-string">"cl100k_base"</span></span>,
  "<span class="hljs-attribute">EMBEDDING_CHUNK_SIZE</span>": <span class="hljs-value"><span class="hljs-number">300</span></span>,
  "<span class="hljs-attribute">NUM_RELATED_QUESTIONS</span>": <span class="hljs-value"><span class="hljs-number">3</span>
</span>}
</code></pre>
</li>
<li class="has-line-data" data-line-start="65" data-line-end="79">
<p class="has-line-data" data-line-start="65" data-line-end="67"><strong>Set up PostgreSQL database:</strong><br>
Ensure you have PostgreSQL installed and running. Create a database named <code>PANNADB</code> and a table named <code>prompt_audit</code> with the following schema:</p>
<pre><code class="has-line-data" data-line-start="68" data-line-end="78" class="language-sql"><span class="hljs-operator"><span class="hljs-keyword">CREATE</span> <span class="hljs-keyword">TABLE</span> prompt_audit (
    <span class="hljs-keyword">time</span> <span class="hljs-keyword">TIMESTAMP</span>,
    <span class="hljs-keyword">prompt</span> <span class="hljs-built_in">TEXT</span>,
    refined_prompt <span class="hljs-built_in">TEXT</span>,
    response <span class="hljs-built_in">TEXT</span>,
    feedback <span class="hljs-built_in">TEXT</span>,
    feedback_comment <span class="hljs-built_in">TEXT</span>,
    channel <span class="hljs-built_in">TEXT</span>
);</span>
</code></pre>
</li>
<li class="has-line-data" data-line-start="79" data-line-end="83">
<p class="has-line-data" data-line-start="79" data-line-end="80"><strong>Start the Django server:</strong></p>
<pre><code class="has-line-data" data-line-start="81" data-line-end="83" class="language-bash">python manage.py runserver
</code></pre>
</li>
<li class="has-line-data" data-line-start="83" data-line-end="87">
<p class="has-line-data" data-line-start="83" data-line-end="84"><strong>Open a new terminal and run the Flask backend:</strong></p>
<pre><code class="has-line-data" data-line-start="85" data-line-end="87" class="language-bash">python backend.py
</code></pre>
</li>
<li class="has-line-data" data-line-start="87" data-line-end="92">
<p class="has-line-data" data-line-start="87" data-line-end="88"><strong>Run the Streamlit app:</strong></p>
<pre><code class="has-line-data" data-line-start="89" data-line-end="91" class="language-bash">streamlit run trainingFE.py
</code></pre>
</li>
</ol>
<h2 class="code-line" data-line-start=92 data-line-end=93 ><a id="Usage_92"></a>Usage</h2>
<ol>
<li class="has-line-data" data-line-start="94" data-line-end="99">
<p class="has-line-data" data-line-start="94" data-line-end="95"><strong>Start the Django server:</strong></p>
<pre><code class="has-line-data" data-line-start="96" data-line-end="98" class="language-bash">python manage.py runserver
</code></pre>
</li>
<li class="has-line-data" data-line-start="99" data-line-end="104">
<p class="has-line-data" data-line-start="99" data-line-end="100"><strong>Open a new terminal and run the Streamlit app:</strong></p>
<pre><code class="has-line-data" data-line-start="101" data-line-end="103" class="language-bash">streamlit run app.py
</code></pre>
</li>
<li class="has-line-data" data-line-start="104" data-line-end="107">
<p class="has-line-data" data-line-start="104" data-line-end="106"><strong>Interact with the chat-bot:</strong><br>
Open your web browser and go to <code>http://localhost:8501</code> to access the Streamlit UI and start interacting with the chat-bot.</p>
</li>
</ol>
<h2 class="code-line" data-line-start=107 data-line-end=108 ><a id="Project_Structure_107"></a>Project Structure</h2>
<p class="has-line-data" data-line-start="109" data-line-end="128">TrainingModule/<br>
├── Training/                # Django app for the chat-bot backend<br>
│   ├── migrations/          # Database migrations<br>
│   ├── <a href="http://models.py">models.py</a>            # Database models<br>
│   ├── <a href="http://views.py">views.py</a>             # Django views<br>
│   ├── <a href="http://urls.py">urls.py</a>              # URL configurations<br>
│   ├── process/             # Folder containing processing files<br>
│   └── …<br>
├── TrainingModule/          # Django project folder<br>
│   ├── <strong>init</strong>.py<br>
│   ├── <a href="http://settings.py">settings.py</a><br>
│   ├── <a href="http://urls.py">urls.py</a><br>
│   ├── <a href="http://wsgi.py">wsgi.py</a><br>
│   └── …<br>
├── <a href="http://backend.py">backend.py</a>               # Flask backend script<br>
├── <a href="http://trainingFE.py">trainingFE.py</a>            # Streamlit frontend script<br>
├── config-dev.json          # Configuration file for API keys<br>
├── requirements.txt         # Python dependencies<br>
└── <a href="http://manage.py">manage.py</a>                # Django management script</p>
<h2 class="code-line" data-line-start=129 data-line-end=130 ><a id="Contributing_129"></a>Contributing</h2>
<p class="has-line-data" data-line-start="131" data-line-end="132">If you would like to contribute to this project, please follow these steps:</p>
<ol>
<li class="has-line-data" data-line-start="133" data-line-end="134">Fork the repository.</li>
<li class="has-line-data" data-line-start="134" data-line-end="135">Create a new branch (<code>git checkout -b feature-branch</code>).</li>
<li class="has-line-data" data-line-start="135" data-line-end="136">Make your changes.</li>
<li class="has-line-data" data-line-start="136" data-line-end="137">Commit your changes (<code>git commit -m 'Add some feature'</code>).</li>
<li class="has-line-data" data-line-start="137" data-line-end="138">Push to the branch (<code>git push origin feature-branch</code>).</li>
<li class="has-line-data" data-line-start="138" data-line-end="139">Open a pull request.</li>
</ol>