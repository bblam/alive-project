from django.shortcuts import renderfrom django.http import HttpResponsefrom django.views import generic, Viewfrom rest_framework.response import Responsefrom rest_framework import status, viewsetsfrom .serializers import *from .models import Session, Userfrom aLive.settings import OPENTOK_API, OPENTOK_SECRETfrom opentok import OpenTokAPI_KEY = OPENTOK_APIAPI_SECRET = OPENTOK_SECRETopentok = OpenTok(API_KEY, API_SECRET)# User can create OpenTok Session# What if ako ning himuon ug read only# then mag create ko ug CreateSessionView(CreateAPIView) ?? HUH ?? HUUUH??class SessionViewSet(viewsets.ModelViewSet):    queryset = Session.objects.all()    serializer_class = SessionSerializer    def create(self, request, *args, **kwargs):        session = opentok.create_session()        req = request.data        if session:            new_session = Session(session_name=req['session_name'],                                  session_id=session.session_id,                                  owner=request.user)            new_session.save()            return Response({'return': 'Successfully created new session'},                            status=status.HTTP_201_CREATED)        return Response({'return': 'Failed to create session'})    def retrieve(self, request, *args, **kwargs):        '''        retrieve method gets called when a user accesses a unique session        user will be given a token to connect to this session        '''        # get current user        user = request.user        print(user)        # get current session        session = self.get_object()        print(session)        # check if session owner ang nag generate sa token        # or check if puno na ang session (max: 2 publishers)        # generate token for current user (default: publisher) valid for 24h        token = opentok.generate_token(session.session_id)        # check if token is created successfully        print(token)        serializer = self.get_serializer(session)        return Response(serializer.data)class SessionDetailView(generic.DetailView):    model = Session    template_name = 'livestream/publish.html'    def get(self, request, *args, **kwargs):        self.object = self.get_object()        context = self.get_context_data(object=self.object)        return self.render_to_response(context)# UserViewSetclass UserViewSet(viewsets.ModelViewSet):    queryset = User.objects.all()    serializer_class = UserSerializer    def create(self, request):        req = request.data        user = User.object.create_user(username=req['username'],                                       password=req['password'],                                       firstname=req['first_name'],                                       lastname=req['last_name'])        if user:            user.save()            return Response(request.data, status=status.HTTP_201_CREATED)        return Response({'return': 'Failed to create new user.'})class ClientTokenViewSet(viewsets.ModelViewSet):    '''        To change:            Tokens should not be stored or reused    '''    queryset = ClientToken.objects.all()    serializer_class = ClientTokenSerializer    def create(self, request):        ret = {'return': 'token creation failed'}        req = request.data        # get session id from db        this_session = Session.objects.get(id=req['session'])        # generate token        token = opentok.generate_token(this_session.session_id)        # get user        user = User.objects.get(id=req['user'])        new_token = ClientToken(token_id=token,                                # fixed wrong parameter thingy                                session=this_session,                                user=user)        # check if new token was successfully created        # and user does not have existing token        print(ClientTokenSerializer(new_token).data)        if new_token:            print(new_token)            # Value error here            new_token.save()            # VALUE ERROR SOLVED            ret = ClientTokenSerializer(new_token).data        return Response(ret)class IndexView(generic.ListView):    template_name = 'livestream/index.html'    context_object_name = 'session_list'    queryset = Session.objects.all()