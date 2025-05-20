## [Triggering Events](https://htmx.org/examples/update-other-content/#events)

To trigger a client side event when a successful contact is created and then listen for that event on the table, causing the table to refresh.

```html
<h2>Contacts</h2>
<table class="table">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th></th>
    </tr>
  </thead>
  <tbody id="contacts-table" hx-get="/contacts/table" hx-trigger="newContact from:body">
    ...
  </tbody>
</table>
<h2>Add A Contact</h2>
<form hx-post="/contacts">
  <label>
    Name
        <input name="name" type="text">  
  </label>
  <label>
    Email
        <input name="email" type="email">  
  </label>
</form>
```

We have added a new end-point `/contacts/table` that re-renders the contacts table. Our trigger for this request is a custom event, `newContact`. We listen for this event on the `body` because when it is triggered by the response to the form, it will end up hitting the body due to event bubbling.

When a successful contact creation occurs during a POST to `/contacts`, the response includes an [HX-Trigger](https://htmx.org/headers/hx-trigger/) response header that looks like this:

```txt
HX-Trigger:newContact
```

This will trigger the table to issue a `GET` to `/contacts/table` and this will render the newly added contact row  
(in addition to the rest of the table.)

Very clean, event driven programming!