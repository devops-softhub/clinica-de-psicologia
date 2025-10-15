from django.db import models

# Create your models here.
class Inscritocomunidade(models.Model):
    ESTADO_CIVIL_CHOICES = [
        ('Solteiro', 'Solteiro'),
        ('Casado', 'Casado'),
        ('Divorciado', 'Divorciado'),
        ('Viúvo', 'Viúvo'),
        ('União Estável', 'União Estável'),
        ('Nenhum', 'Nenhum'),
        ('Outros', 'Outros'),
    ]

    IDENTIDADE_GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Não Binário', 'Não Binário'),
        ('Transgênero', 'Transgênero'),
        ('Outros', 'Outros'),
    ]

    ETNIA_CHOICES = [
        ('Branca', 'Branca'),
        ('Preta', 'Preta'),
        ('Parda', 'Parda'),
        ('Amarela', 'Amarela'),
        ('Indígena', 'Indígena'),
        ('Outras', 'Outras'),
    ]

    RELIGIAO_CHOICES = [
        ('Católico', 'Católico'),
        ('Evangélico', 'Evangélico'),
        ('Budismo', 'Budismo'),
        ('Espirita', 'Espirita'),
        ('Hinduísmo', 'Hinduísmo'),
        ('Islamismo', 'Islamismo'),
        ('Judaismo', 'Judaismo'),
        ('Religião de Matriz Africana', 'Religião de Matriz Africana'),
        ('Sem religião', 'Sem religião'),
        ('Outros', 'Outros'),
    ]

    idfichacomunidade = models.AutoField(primary_key=True)
    nomeinscrito = models.CharField(max_length=100)
    dtnascimento = models.DateField()
    nomeresp = models.CharField(max_length=50, blank=True, null=True)
    grauresp = models.CharField(max_length=25, blank=True, null=True)
    cpfresp = models.CharField(max_length=11, unique=True, blank=True, null=True)
    estadocivilresp = models.CharField(max_length=25, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    tellcellresp = models.CharField(max_length=20, blank=True, null=True)
    emailresp = models.CharField(max_length=45, blank=True, null=True)
    estadocivilinscrito = models.CharField(max_length=25, choices=ESTADO_CIVIL_CHOICES)
    cpfinscrito = models.CharField(max_length=11, unique=True)
    tellcellinscrito = models.CharField(max_length=20)
    contatourgencia = models.CharField(max_length=15)
    nomecontatourgencia = models.CharField(max_length=50)
    emailinscrito = models.CharField(max_length=45)
    identidadegenero = models.CharField(max_length=25, choices=IDENTIDADE_GENERO_CHOICES)
    etnia = models.CharField(max_length=15, choices=ETNIA_CHOICES)
    religiao = models.CharField(max_length=30, choices=RELIGIAO_CHOICES)
    confirmlgpd = models.BooleanField(default=False)
    dthinscricao = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nomeinscrito
    
    class Meta:
        managed = False
        db_table = 'inscritocomunidade'


class Medicamento(models.Model):
    idmedicamento = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey(Inscritoconvenio, models.DO_NOTHING, db_column='idfichaconvenio', blank=True, null=True)
    idfichacomunidade = models.ForeignKey(Inscritocomunidade, models.DO_NOTHING, db_column='idfichacomunidade', blank=True, null=True)
    ansiolitico = models.BooleanField(blank=True, null=True)
    antidepressivo = models.BooleanField(blank=True, null=True)
    antipsicotico = models.BooleanField(blank=True, null=True)
    estabhumor = models.BooleanField(blank=True, null=True)
    memoriatct = models.BooleanField(blank=True, null=True)
    outro = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicamento'

class Endereco(models.Model):
    idendereco = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey('Inscritoconvenio', models.DO_NOTHING, db_column='idfichaconvenio', blank=True, null=True)
    idfichacomunidade = models.ForeignKey('Inscritocomunidade', models.DO_NOTHING, db_column='idfichacomunidade', blank=True, null=True)
    cidade = models.CharField(max_length=40)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    rua = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, default='DF')
    cep = models.CharField(max_length=10, unique=True)

    class Meta:
        managed = False
        db_table = 'endereco'

class Doencafisica(models.Model):
    iddoencafisica = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey('Inscritoconvenio', models.DO_NOTHING, db_column='idfichaconvenio', blank=True, null=True)
    idfichacomunidade = models.ForeignKey('Inscritocomunidade', models.DO_NOTHING, db_column='idfichacomunidade', blank=True, null=True)
    doencaresp = models.BooleanField(blank=True, null=True)
    cancer = models.BooleanField(blank=True, null=True)
    diabete = models.BooleanField(blank=True, null=True)
    disfusexual = models.BooleanField(blank=True, null=True)
    doencadgt = models.BooleanField(blank=True, null=True)
    escleorosemlt = models.BooleanField(blank=True, null=True)
    hcpt = models.BooleanField(blank=True, null=True)
    luposatm = models.BooleanField(blank=True, null=True)
    obesidade = models.BooleanField(blank=True, null=True)
    pblmarenal = models.BooleanField(blank=True, null=True)
    outro = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doencafisica'

class Motivoacompanhamento(models.Model):
    idmotivoacamp = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey(Inscritoconvenio, models.DO_NOTHING, db_column='idfichaconvenio', blank=True, null=True)
    idfichacomunidade = models.ForeignKey(Inscritocomunidade, models.DO_NOTHING, db_column='idfichacomunidade', blank=True, null=True)
    ansiedade = models.BooleanField(blank=True, null=True)
    assediomoral = models.BooleanField(blank=True, null=True)
    depressao = models.BooleanField(blank=True, null=True)
    dfaprendizagem = models.BooleanField(blank=True, null=True)
    humorinstavel = models.BooleanField(blank=True, null=True)
    insonia = models.BooleanField(blank=True, null=True)
    isolasocial = models.BooleanField(blank=True, null=True)
    luto = models.BooleanField(blank=True, null=True)
    tristeza = models.BooleanField(blank=True, null=True)
    apatia = models.BooleanField(blank=True, null=True)
    chorofc = models.BooleanField(blank=True, null=True)
    exaustao = models.BooleanField(blank=True, null=True)
    fadiga = models.BooleanField(blank=True, null=True)
    faltanimo = models.BooleanField(blank=True, null=True)
    vldt = models.BooleanField(blank=True, null=True)
    assediosexual = models.BooleanField(blank=True, null=True)
    outro = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motivoacompanhamento'

class Pcdsnd(models.Model):
    idpcdnd = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey(Inscritoconvenio, models.DO_NOTHING, db_column='idfichaconvenio', blank=True, null=True)
    idfichacomunidade = models.ForeignKey(Inscritocomunidade, models.DO_NOTHING, db_column='idfichacomunidade', blank=True, null=True)
    tea = models.BooleanField(blank=True, null=True)
    tdah = models.BooleanField(blank=True, null=True)
    dffs = models.BooleanField(blank=True, null=True)
    dfv = models.BooleanField(blank=True, null=True)
    dfa = models.BooleanField(blank=True, null=True)
    ttap = models.BooleanField(blank=True, null=True)
    ahst = models.BooleanField(blank=True, null=True)
    outro = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pcdsnd'

class Tipoterapia(models.Model):
    idtipoterapia = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey(
        Inscritoconvenio, 
        models.DO_NOTHING, 
        db_column='idfichaconvenio', 
        blank=True, 
        null=True
    )
    idfichacomunidade = models.ForeignKey(
        Inscritocomunidade, 
        models.DO_NOTHING, 
        db_column='idfichacomunidade', 
        blank=True, 
        null=True,
        related_name='tipoterapias'  # aqui, nome plural para o reverse lookup
    )
    individualift = models.BooleanField(blank=True, null=True)
    individualadt = models.BooleanField(blank=True, null=True)
    individualadto = models.BooleanField(blank=True, null=True)
    individualids = models.BooleanField(blank=True, null=True)
    familia = models.BooleanField(blank=True, null=True)
    grupo = models.BooleanField(blank=True, null=True)
    casal = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipoterapia'

class Disponibilidade(models.Model):
    iddisponibilidade = models.AutoField(primary_key=True)
    idfichaconvenio = models.ForeignKey(
        'Inscritoconvenio',
        models.DO_NOTHING,
        db_column='idfichaconvenio',
        blank=True,
        null=True
    )
    idfichacomunidade = models.ForeignKey(
        'Inscritocomunidade',
        models.DO_NOTHING,
        db_column='idfichacomunidade',
        blank=True,
        null=True,
        related_name='disponibilidades'  # nome plural para evitar conflito
    )
    manha = models.BooleanField(blank=True, null=True)
    tarde = models.BooleanField(blank=True, null=True)
    noite = models.BooleanField(blank=True, null=True)
    sabado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disponibilidade'