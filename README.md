                                                                       
                                    ETAPE DE CREATION D'UNE API_PYTHON

NB : Les developpeurs travaillent sur les apis en backend.
     les utilisateurs vont utiliser le frontend ou client. qui consomment les api

ETAPE 1: Creation d'une environnement virtuelle (python3 -m venv venv): l'activer avec source venv/bin/activate
ETAPE 2: dans venv creer un fichier requirements et y mettre tout
         ce qu'on aurra besoin d'utiliser
        
        Installer les requirements si non Installer avec pip installe -r requirements.txt

ETAPE 3: entrer dans le package backend, y creer un projet dans le terminal avec la com-
         mande django-admin startproject core .

ETAPE 4: Toujours dans backend creer une application la commande django-admin startapp 
          nom_de_l'application

Conseil : ouvrir deux terminal; l'un pour le backend et l'autre pour le test de reussite sur 
        le frontend

ETAPE 5 : Dans le core du backend, ouvrir le fichier settings.py, trouver la partie
        INSTALLEDS_APPS, et ajouter a la fin le nom de notre repertoire de 
        l'application local(son dossier)
        => api est notre dossier local ici

ETAPE 6 : retour dans le dossier api, y ajouter un fichier api ou urls.py precisement.

ETAPE 7 : Ouvrir ce fichier et y implementer notre premier code.
          en premier import path du package django.urls

     urls.py <== [  // contenu
          apres l'importation, on y cree une liste vide dite <<urlpatterns>>.
     ]

ETAPE 8 : retour dans le dossier core, ouvrir son fichier urls.py.
          a la ligne d'importation path du package django.urls, y ajouter include pour
          prendre en compte le comportement de l'api urls.py du package api.

          toujours dans le meme fichier, dans la liste urlpatterns, ajouter en deuxieme ligne
          le chemin vers le fichier urls.py du package api.

     core/urls.py <== {
          ... code recent.
          path('api/', include('api.urls'))
     }    

ETAPE 9 : Implementation des donnees a retourner au format json 
          ==> Ouvrir le package api, ouvrir le fichier views.py
          => from django.http on y importe le package JsonResponse
          et apres l'importation.
     
     views.py <== {
          on defini une fonction home avec comme parametre requete, et type de retour
          JsonResponse("qui est soit un string, tuple, dictionnaire, ...")
     }

ETAPE 10 : Reouvrir le fichier urls.py du meme package(api), mettre dans notre liste 
           l'object retourner par home premier y tapper la commande from .views import home
           Apres cette import, ajouter dans la liste urlpatterns la fonction d'objets home
           => path('', home, name='home')

     NB : pour faire un peut du test au niveau du client(package client), creons un fichier 
          test.py parexemple
          y importer la bibliotheque request;
          
          >> cree une variable endpoint, y assigner le lien de notre package api, car il 
             contien urls.py qui est executer par les donnees de urls.py du core package.
               /// explication simple aller dans le urls.py du package api,
               recupere le lien d'execution dans ce package, a la ligne ou on trouve le chemin 'api/' et 
               afficher les donnee qui y  sont

          ExSyntaxe : endpoint = http://localhost:8000/api
                    ne jamais utiliser https sur le serveur manage.py, il ne le supporte pas

     ici, une erreur de connexion est bien lever comme nous n'avons pas bien prix soin de demar_
     rer un serveur avant d'executer notre code.
     Pour se faire, nous demarons le serveur manage.py du package core.
     => python3 manage.py runserver a l'emplacement du fichier

     pour passer les donnee dans la variable "parms" qui a la methode GET, je vais ouvrir mon fichier
     de test, dans le endpoint le lien qui y est affecter j'ajoute a la fin apres le dossier api,
     un le character special "?".

     ce point d'interrogation suivi de q= i.e query=: pour faire une recherche sur le web
          syntaxe = 'http://localhost:8000/api/?q=donaldprogrammeur'; vas faire la recherche sur
          cette page.

          si l'on veut l'afficher comme valeur de retour dans dans home, => les donnees du frontend
          que client verra. Aller dans le fichier ../api/urls.py dans la variable params, recuperer 
          les donnees avec la fonction get() et le character 'q' en parametre.
          => params = request.GET.get('q')

ETAPE 11 : Creation d'une base des donnee, comme le headers nous renvoie les donnee du type text/plain
           et que nous voulons bien les traiters.
           On ouvre le fichier models.py du package api.

          Y creer une classe production, qui herite Model du package models:
          - initialiser une variable name qui stoque les noms dans la fonction models.CharField avec
            une taille de character max a 255 en parametre.
          - initialiser une variable price avec models.DecimalField en parametre une max_digits de 10 et 
            decimal_places de 2
          - initialiser une variable description avec models.TextField
          - initialiser une variable de Creation automatique avec models.DateTimeField a parametre 
            auto_now_add un boolean true
          - initialiser une variable de misajour automatique avec models.DateTimeField a parametre
            auto_now.

          et une classe string qui retourne name.
          models.py <== {
               class Product(models.Model)
                    //... le code precedant

                    def __str__(self):
                         return self.name
          }

          apres avoir creer cette classe, on peut faire la migration dans le terminal avec:
               python3 manage.py makemigrations un fichier 0001_initial.py creer automatiquement
               puis taper python3 manage.py migrate pour faire migrer
               Nous pouvons alors reexecuter le serveur.

               CAS DU POST

ETAPE 12 : creation d'une autre class dans ../client pour faire un post
           Ex: creat_product.py on y import requests, puis nous sauvegardons toujours le meme endpoint.
          
          creer un dictionnaire de datas par exemple, et y mettre toute les donnees qui doivent etre envoyer
          i.e celles que l'on a signaler a la base des donnees (name, price, description)

          envoyer les produits a la base des donnee avec la fonction post, ayant en parametre notre endpoint,
          et une variable data ou l'on affecte notre dictionnaire des produits. 

          pour permettre que ca puisse les posters, nous allons changer l'etat de la variable post_data,
          en request.body et si l'on veut afficher le message du coter serveur en character visible, nous
          pouvons l'encoder en utf-8 
          => request.body.decode('utf-8')

     NB: ici l'erreur de CSRF est generer du coter serveur(backend) => nous devons importer un csrf.token,
          comme c'est un site developper avec django.
          Le CSRF : permet de
          securiser les donnees transferees; or le client(Developpeur ou entreprise)
          qui va utiliser mon api ne sera pas capable de generer ce csrf.token (Car c'est notre application
          qui le gere).
          ==> views.py de ../api/ <== {
               from django.views.decorator.csrf import csrf_exempt

               // tout en haut avant la declaration de la fonction home, ajouter @csrf_exempt
               => @csrf_exempt
               def home(request):
                    ....reste du code
          }

          le csrf (csrf_exempt): permet de sauter l'etape de la verification du csrf.token.

     On est obliger d'utilser le csrf.token car c'est un api qui sera public, ON ARRAIT GENERER NOTRE PROPRE
     CSRF.TOKEN, SI ON A BESOIN D'UN CSRF.TOKEN SI SON UTILISATION VAS ETRE PRIVATE.

ETAPE 13 : On veut importer le produit qui a ete creer tout simplement apartir de la classe models du 
           package .../api, alors on n'import product dans views.py puis mettre cette sytaxe.

               {
                    if request.method == 'POST':
                         post_data = request.body.decode('utf-8')

                         # pour convertir le JSON en dictionnaire
                         # en enlevant les format bytes b'' des post_data
                         data = json.loads(post_data) if post_data else {}

                         name = data.get('name')
                         price = data.get('price')
                         description = data.get('description')

                         product = Product.objects.create(
                              name=name
                              price=price
                              description=description
                         )
                         return JsonResponse({
                              'name':product.id
                              'price':product.name
                              'description':product.description
                         })
                    si rien a etait donnee
                    products = Product.objects.all()
                    data =[{'id':product.id, 'name':product.name, ...} for product in products]

                    en suite nous retournons.
                    return JsonResponse(data)
                }

                         CAS DU GET
          En alevant le json=data dans le fichier creat_product, une erreur se leve, avec la 
          compatibiliter du type des datas, cssons la SECURITE en false dans le retour de la fonction
          home de la class creat_product, comme on ne peut jamais serealiser en jso une liste seulment
          un dictionnaire.

          toujours signaler l'operation que l'on s'apprette a faire soit:
               request.post(endpoint, data ou json=data)
               request.get(endpoint)

     Ainsi donc cette opperation ou proceder d'avoir les objects et les envoyes sous format json est la 
     la serealisation(post) ou request.post(endpoint, data ou json=data) et son operation inverse est du
     format json en objects python est appeler la deserealisation request.get(endpoint).

     Le probleme avec les api rest de django est que nous ecrivons tout manuellement les csrf, la sereali-
     sation, meme pour la validation dans la fonction home de la classe views.py pour verifier la compati-
     biliter du type presque tout le code.
     => trop des manipulation
     D'ou nous devons utiliser, django rest framework qui est un frame work flexible

ETAPE 14 : maintenant faisons le django rest framework, pour ce faire, nous allons premierement dans le settings
           dossier core.
           juste dans INSTALLED_APP, ajoutons la ligne de code "rest-framework"
           puis dans le package backend/api, on cree un sous package du nom de api. et dans ce package, nous allons creer deux 
           fichier, l'un appeller api.py, et l'autre serializers.py

           Dans le fichier api.py, 
           on vas importer le Product de api.models,
           en suite from rest_framework.response import Response 
               Remarque: Si un Warning est lever verifier tout simplement si l'environnement de python est bien sec.
                         pour verifier cliquez sur le warnig et suivez les instructions

           en suite nous importons api_view de la bibliotheque rest_framework.decorators
           cette bibliotheque vas nous permettre de voir comment develloper une api rest avec view
           => toujours dans le rest_framework, nous importons aussi status

           A la ligne suivante, nous allons taper @api_view(['GET', 'POST']) tout juste apres les importations.
           determinons apres une foction tout juste en bas dite prodoc_api_view(request)

           comme on aimerais pas faire une serialization manuelle avec un object de retour qui est Response,
           "if request.method == 'GET':
               products = Product.objects.all()
               product_data = [{"id": product.id, "name": product.name, "price": product.price} for product in products]
               return Response(product_data, status=status.HTTP_200_OK) " 
        alors nous entrons dans la classe serializers.py

        Une fois dedans, dans la classe models du api, nous importons Product.
        puis importer les serializers du rest_framework qui sont des formulaires.
        Puis la classe Product_Serializers qui implemente le ModelSerializers de serializers
        puis meton un classe imbriquer meta, ayant comme variables model = Product et fields = _all_
        i.e qu'ici le model ou produit, vas s'executer sur tout le champ automatiquement.

        On pourrait aussi le personaliser si on le veux, mais la classe vas implementer seulement serializers.Serializers

        => retour dans le fichier api dans le meme package et importons notre classe de serialisation
          [from .api.api.serializers import Product_Serializers1]

     Toujours se rassurer que l'environnement est activer pour demarrer le serveur python3

     n'ajoute jamais une variable de methode qui n'est pas dans le models.py
          Exemple : ajouter le champs d'email dans la class serializers.py pourrait generer un erreur s'il n'est pas reconnu
                    par la class modeles comme etant un produit.

          Sauf si l'on fait la surcharge de la metode create dans la classe serializers.

ETAPE 15 : validation de s donnees
           Nous povons ajouter les methodes PUT, DELE
