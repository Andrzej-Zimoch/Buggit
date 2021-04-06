var ticket_element = document.getElementsByClassName("ticket");
var len = ticket_element.length;

var cur_id = 0;

while ( cur_id < len)
{
    ticket_element[cur].id="drag"+cur
    cur++;
}