document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-submit').addEventListener('click', submit_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function f_archive(email){

  // To archive or unarchive emails
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived
    })
  })
  .then(document.location.reload(true))
  .then(load_mailbox('inbox'))

}

function reply_email(email){

  // Default values
  
  document.querySelector('#title').innerHTML = 'Reply Email';
  document.querySelector('#compose-recipients').value = email.sender;
  
  if (email.subject.substring(0,3) != 'Re:'){
    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
  } else {
    document.querySelector('#compose-subject').value = email.subject;
  }

  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // See for emails clustered by state
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
    // Print emails
    // console.log(emails);
    
      for (let i of Object.keys(emails)){
        const email_list = document.createElement('div');
        if (emails[i].read){
          email_list.innerHTML = `<div class="row">
            <div class="col-sm-9" id="read">
              ${emails[i].subject}
              <div class="row">
                <div class="col-xs-8 col-sm-6">
                  ${emails[i].sender}
                </div>
                <div class="col-xs-4 col-sm-6">
                  ${emails[i].timestamp}
                </div>
              </div>
            </div>
          </div>`;
        } else {
          email_list.innerHTML = `<div class="row">
          <div class="col-sm-9" id="unread">
            ${emails[i].subject}
            <div class="row">
              <div class="col-xs-8 col-sm-6">
                ${emails[i].sender}
              </div>
              <div class="col-xs-4 col-sm-6">
                ${emails[i].timestamp}
              </div>
            </div>
          </div>
        </div>`;
        }
        email_list.addEventListener('click', () => see_email(emails[i].id, mailbox));
        document.querySelector('#emails-view').append(email_list);
      };
  });

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function submit_email(event) {

  event.preventDefault();
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: compose_recipients,
        subject: compose_subject,
        body: compose_body
    })
  })
  .then(response => response.json())
  .then(result => {
    localStorage.clear();
    load_mailbox('sent');
    return false;
  });
}

function see_email(email_id, mailbox) {

  // To change the read variable of an email
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // See for a clicked email
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Template for clicked email
      document.querySelector('#email-view').innerHTML = `<h2>${email.subject}</h2>
      <p style="text-align:left;">
        sender: ${email.sender}
        <span style="float:right;">
          ${email.timestamp}
        </span><br>
        from: ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}
        <br>
        ${email.body}
      </p>`;

      let buttons = document.createElement('div');
      buttons.classList.add('outer');
      
      const unarch = document.createElement('div');
      unarch.classList.add('inner');
      unarch.innerHTML = `<button id="unarch" type="submit" class="btn btn-sm btn-primary">Unarchive</button>`;

      const arch = document.createElement('div');
      arch.classList.add('inner');
      arch.innerHTML = `<button id="arch" type="submit" class="btn btn-sm btn-primary">Archive</button>`;

      const reply = document.createElement('div');
      reply.classList.add('inner');
      reply.innerHTML = `<button id="reply" type="submit" class="btn btn-sm btn-secondary">Reply</button>`
      reply.addEventListener('click', () => reply_email(email));

      if (email.sender != email.user_id){
        if (email.archived){
          unarch.addEventListener('click', () => f_archive(email));
          buttons.appendChild(unarch);
          buttons.appendChild(reply);
        } else {
          arch.addEventListener('click', () => f_archive(email));
          buttons.appendChild(arch);
          buttons.appendChild(reply);
        }
      } else {
        buttons.appendChild(reply);
      }
      document.querySelector('#email-view').append(buttons);
      localStorage.clear();
    });

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
}