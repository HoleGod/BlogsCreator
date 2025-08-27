<h2>About BlogsCreator</h2>
<strong>BlogsCreator</strong> is a simple yet powerful web application for <strong>creating, editing, viewing, and deleting blog posts</strong>. 
Users can upload images for posts, and each post is linked to an author. The project demonstrates core web development principles including user authentication, file uploads, and database integration.

The application is built with <strong>Flask</strong> (a lightweight Python web framework) and uses <strong>PostgreSQL</strong> as the database backend. Uploaded images are securely saved on the server and displayed alongside post content.

<hr>

<h2>Technologies:</h2>
<ul>
  <li>Python;</li>
  <li>Flask;</li>
  <li>PostgreSQL;</li>
  <li>psycopg2 (PostgreSQL adapter);</li>
  <li>Jinja2 templates;</li>
  <li>Werkzeug (for secure file handling);</li>
  <li>HTML + CSS;</li>
</ul>

<hr>

<h2>How to install the project?</h2>
<h3>Server side setup:</h3>
<ol>
  <li>Clone the repository and navigate into the project directory;</li>
  <li>(Optional) Create and activate a Python virtual environment:
    <code>python -m venv venv</code> and <code>source venv/bin/activate</code> (or <code>venv\Scripts\activate</code> on Windows);
  </li>
  <li>Install required dependencies:
    <code>pip install -r requirements.txt</code>;
  </li>
  <li>Create a <code>.env</code> file in the root directory with your PostgreSQL credentials:
    <pre>
HOST=your_database_host
DBNAME=your_database_name
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
    </pre>
  </li>
  <li><strong>Set up PostgreSQL server and database:</strong>
    <ol>
      <li>Install PostgreSQL if not already installed (see <a href="https://www.postgresql.org/download/">official site</a>);</li>
      <li>Access PostgreSQL prompt via terminal or pgAdmin;</li>
      <li>Create a new database:
        <pre>CREATE DATABASE your_database_name;</pre>
      </li>
      <li>Create a user with password:
        <pre>CREATE USER your_db_username WITH PASSWORD 'your_password';</pre>
      </li>
      <li>Grant privileges to the user on the database:
        <pre>GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_db_username;</pre>
      </li>
    </ol>
  </li>
  <li>Run the Flask development server with debug mode:
    <code>python3 -m flask --app Blog run --debug</code>;
  </li>
  <li>Open your browser and navigate to <code>http://localhost:5000</code> to access the blog.</li>
</ol>

<hr>

<h2>Image Uploads:</h2>
<ul>
  <li>Allowed formats: PNG, JPG, JPEG, GIF;</li>
  <li>Images are stored in the <code>static/uploads</code> folder;</li>
  <li>A default image is shown if no image is provided for a post.</li>
</ul>

<hr>

<h2>Routes Overview:</h2>
<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Route</th>
    <th>Method(s)</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/</code></td>
    <td>GET</td>
    <td>Home page showing all blog posts</td>
  </tr>
  <tr>
    <td><code>/post/&lt;post_id&gt;</code></td>
    <td>GET</td>
    <td>View a specific post</td>
  </tr>
  <tr>
    <td><code>/post/create</code></td>
    <td>GET, POST</td>
    <td>Create a new post (login required)</td>
  </tr>
  <tr>
    <td><code>/post/&lt;post_id&gt;/edit</code></td>
    <td>GET, POST</td>
    <td>Edit an existing post (login required)</td>
  </tr>
  <tr>
    <td><code>/post/&lt;post_id&gt;/delete</code></td>
    <td>POST</td>
    <td>Delete a post (login required)</td>
  </tr>
</table>
