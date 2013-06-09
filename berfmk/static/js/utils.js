function update_preview(id_preview, id_field, def)
{
    document.getElementById(id_preview).textContent = document.getElementById(id_field).value || def;
}
