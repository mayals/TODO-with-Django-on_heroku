console.log('hello world')

//this function only try    -- not work !!
function task_edit_link() {
    var task_id = document.getElementById("task_id").val;

    return "/edit/<int:" + task_id + ">/";
}