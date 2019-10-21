<?php

require_once __DIR__."/dtos/GemeinsameBuchungDto.php";
/**
 * @Entity @Table(name="gemeinsamebuchungen")
 **/
class GemeinsameBuchung
{
    /** @Id @Column(type="integer") @GeneratedValue **/
    protected $id;
    /** @Column(type="string") **/
    protected $name;
    /** @Column(type="string") **/
    protected $user;
    /** @Column(type="string") **/
    protected $zielperson;
    /** @Column(type="string") **/
    protected $kategorie;
    /** @Column(type="date") **/
    protected $datum;
    /** @Column(type="decimal") **/
    protected $wert;

    public function getName()
    {
        return $this->name;
    }

    public function getKategorie()
    {
        return $this->kategorie;
    }

    public function getDatum()
    {
        return $this->datum;
    }

    public function getWert()
    {
        return $this->wert;
    }

    public function getUser()
    {
        return $this->user;
    }

    public function getZielperson()
    {
        return $this->zielperson;
    }

    public function setName($name) { $this->name = $name;}
    public function setKategorie($kategorie) { $this->kategorie = $kategorie;}
    public function setUser($user) { $this->user = $user;}
    public function setDatum($datum) { $this->datum = $datum;}
    public function setWert($wert) { $this->wert = $wert;}
    public function setZielperson($zielperson) { $this->zielperson = $zielperson;}

    public function asDto() {
	$dto = new GemeinsameBuchungDto();
	$dto->id = $this->id;
	$dto->datum = $this->getDatum()->format('Y-m-d');
	$dto->name = $this->getName();
	$dto->kategorie = $this->getKategorie();
	$dto->wert = $this->getWert();
	$dto->user = $this->getUser();
	$dto->zielperson = $this->getZielperson();
	return $dto;
    }
}
