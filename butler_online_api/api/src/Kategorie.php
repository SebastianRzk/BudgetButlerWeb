<?php
/**
 * @Entity @Table(name="kategorie")
 **/
class Kategorie
{
    /** @Id @Column(type="integer") @GeneratedValue **/
    protected $id;
    /** @Column(type="string") **/
    protected $name;
    /** @Column(type="string") **/
    protected $user;

    public function getName()
    {
        return $this->name;
    }

    public function getWert()
    {
        return $this->wert;
    }

    public function asDto() {
	return $this->name;
    }
}
