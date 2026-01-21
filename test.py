import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

# 1️⃣ Configurer la clé API Brevo
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'
api_client = sib_api_v3_sdk.ApiClient(configuration)
email_api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

# 2️⃣ Créer le mail (envoyé à toi-même)
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
    to=[{"email": "michaellapeyrere.ml@gmail.com", "name": "Michael"}],  # toi
    sender={"email": "michaellapeyrere.ml@gmail.com", "name": "Visiteur du site"},  # adresse validée
    reply_to={"email": "michael.lapeyrere@gmail.com", "name": "Lapeyrère Michaël"},  # adresse du visiteur
    subject="Nouveau message depuis le site",
    html_content=f"""
        <h2>Nouveau message reçu :</h2>
        <p><b>Nom :</b> "Lapeyrère Michaël"</p>
        <p><b>Email :</b> "michael.lapeyrere@gmail.com"</p>
        <p><b>Message :</b> "Je fais un test"</p>
    """
)

# 3️⃣ Envoyer le mail
try:
    response = email_api.send_transac_email(send_smtp_email)
    pprint(response)
    print("Mail envoyé dans ta boîte Gmail !")
except ApiException as e:
    print("Exception: %s\n" % e)