from django.db import models


# tabela coordenador do banco de dados
class Coordenador(models.Model):
    idcoordenador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    senha = models.CharField(max_length=255)
    cpf = models.CharField(unique=True, max_length=11)
    crp = models.IntegerField(unique=True)
    crpcoord = models.ForeignKey('self', models.DO_NOTHING, db_column='crpcoord', to_field='crp', blank=True, null=True)
    dthcoord = models.DateTimeField()
    emailinst = models.CharField(max_length=255)
    status = models.BooleanField(blank=True, null=True)
    # verificar ser a tabela existe no BD e caso não criar a tabela no banco de dados.
    class Meta:
        managed = False
        db_table = 'coordenador'

class Estagiario(models.Model):
    idestagiario = models.AutoField(primary_key=True)
    crpsup = models.ForeignKey('Supervisor', models.DO_NOTHING, db_column='crpsup', to_field='crp')
    crpcoord = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='crpcoord', to_field='crp')
    nome = models.CharField(max_length=50)
    ra = models.IntegerField(unique=True)
    senha = models.CharField(max_length=10)
    nivelestagio = models.CharField(max_length=10)
    semestre = models.CharField(max_length=10)
    emailinst = models.CharField(max_length=255)
    dthestg = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    # verificar ser a tabela existe no BD e caso não criar a tabela no banco de dados.
    class Meta:
        managed = False
        db_table = 'estagiario'


class Resptec(models.Model):
    idresptec = models.AutoField(primary_key=True)
    crpcoord = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='crpcoord', to_field='crp')
    nome = models.CharField(max_length=50)
    senha = models.CharField(max_length=255)
    cpf = models.CharField(unique=True, max_length=11)
    crpresp = models.IntegerField(unique=True)
    dthresp = models.DateTimeField()
    emailinst = models.CharField(max_length=255)
    status = models.BooleanField(blank=True, null=True)
    # verificar ser a tabela existe no BD e caso não criar a tabela no banco de dados.
    class Meta:
        managed = False
        db_table = 'resptec'

class Secretaria(models.Model):
    idsecretaria = models.AutoField(primary_key=True)
    crpcoord = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='crpcoord', to_field='crp')
    nome = models.CharField(max_length=50)
    cpf = models.CharField(unique=True, max_length=11)
    codfuncionario = models.IntegerField(unique=True)
    senha = models.CharField(max_length=255)
    dthsec = models.DateTimeField()
    emailinst = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    # verificar ser a tabela existe no BD e caso não criar a tabela no banco de dados.
    class Meta:
        managed = False
        db_table = 'secretaria'

class Supervisor(models.Model):
    idsupervisor = models.AutoField(primary_key=True)
    crpcoord = models.ForeignKey(Coordenador, models.DO_NOTHING, db_column='crpcoord', to_field='crp')
    nome = models.CharField(max_length=50)
    cpf = models.CharField(unique=True, max_length=11)
    crp = models.IntegerField(unique=True)
    senha = models.CharField(max_length=255, blank=True, null=True)
    emailinst = models.CharField(max_length=255, blank=True, null=True)
    dthsup = models.DateTimeField()
    status = models.BooleanField(blank=True, null=True)
    # verificar ser a tabela existe no BD e caso não criar a tabela no banco de dados.
    class Meta:
        managed = False
        db_table = 'supervisor'
# Create your models here.
