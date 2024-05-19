//Formulario de admin

new MultiSelectTag('ingredientes', {
    rounded: true,    
    shadow: true,      
    placeholder: 'Busca ingredientes',  
    tagColor: {
        textColor: '#327b2c',
        borderColor: '#92e681',
        bgColor: '#eaffe6',
    },
    onChange: function(values) {
        console.log(values)
    }
})