

##adicionar uma nova aplicacao 
{% for app in apps %}
<div class="rectangle">
    <img src="{{ app.image }}" alt="{{ app.title }}">
    <div class="text">
        <h2>{{ app.title }}</h2>
        <p>{{ app.description }}</p>
    </div>
    <p class="android-icon"><i class="fab fa-android" onclick="openModal('modal1')"></i></p>
</div>
{% endfor %}

##adicionar uma nova ferramenta



##adicionar um novo recurso





